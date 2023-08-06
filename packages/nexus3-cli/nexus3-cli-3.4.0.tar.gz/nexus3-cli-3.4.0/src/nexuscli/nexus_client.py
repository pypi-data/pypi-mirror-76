import json
import logging
import os
import pathlib
import sys

import requests
import semver
from clint.textui import progress
from urllib.parse import urljoin
from typing import Dict, Iterator, Optional

from nexuscli.nexus_config import NexusConfig
from nexuscli import exception, nexus_util
from nexuscli.api.cleanup_policy import CleanupPolicyCollection
from nexuscli.api.repository import RepositoryCollection, Repository
from nexuscli.api.security.realms import RealmCollection
from nexuscli.api.script import ScriptCollection
from nexuscli.api.task import TaskCollection

LOG = logging.getLogger(__name__)


class NexusClient:
    """
    A class to interact with Nexus 3's API.

    Unless all keyword arguments ``url``, ``user`` and ``password`` are
    supplied, the class will attempt to read the configuration file and,
    if unsuccessful, use defaults.

    Args:
        config: instance containing the configuration for the
            Nexus service used by this instance.
    """
    def __init__(self, config: NexusConfig = None):
        self.config: NexusConfig = config or NexusConfig()
        self._local_sep = os.sep
        self._server_version: Optional[str] = None
        # Collections
        self._cleanup_policies: Optional[RealmCollection] = None
        self._repositories: Optional[RepositoryCollection] = None
        self._scripts: Optional[ScriptCollection] = None
        self._security_realms: Optional[RealmCollection] = None
        self._tasks: Optional[TaskCollection] = None

        self.repositories.refresh()

    @property
    def server_version(self) -> Optional[semver.VersionInfo]:
        """
        Parse the Server header from a Nexus request response and return
        as version information. The method expects the header Server to be
        present and formatted as, e.g., 'Nexus/3.19.1-01 (OSS)'

        :return: the parsed version. If it can't be determined, return None.
        :rtype: Union[None,semver.VersionInfo]
        """
        if self._server_version is None:
            response = self.http_get(self.config.url)

            if response.status_code != 200:
                raise exception.NexusClientAPIError(response.reason)

            server = response.headers.get('Server')

            if server is None:
                return None

            try:
                maybe_semver = server.split(' ')[0].split('/')[1].split('-')[0]
                version = semver.VersionInfo.parse(maybe_semver)
            except (IndexError, ValueError):
                return None

            self._server_version = version
        return self._server_version

    @property
    def repositories(self) -> RepositoryCollection:
        """
        Instance of
        :class:`~nexuscli.api.repository.collection.RepositoryCollection`. This
        will automatically use the existing instance of :class:`NexusClient` to
        communicate with the Nexus service.
        """
        if self._repositories is None:
            self._repositories = RepositoryCollection(client=self)
        return self._repositories

    @property
    def security_realms(self) -> RealmCollection:
        """
        This instance uses the existing instance of :class:`NexusClient` to communicate with the
        Nexus service.
        """
        if self._security_realms is None:
            self._security_realms = RealmCollection(client=self)
        return self._security_realms

    @property
    def tasks(self) -> TaskCollection:
        """
        Instance of
        :class:`~nexuscli.api.task.collection.RepositoryCollection`. This
        will automatically use the existing instance of :class:`NexusClient` to
        communicate with the Nexus service.
        """
        if self._tasks is None:
            self._tasks = TaskCollection(client=self)
        return self._tasks

    @property
    def cleanup_policies(self) -> CleanupPolicyCollection:
        """
        Instance of
        :class:`~nexuscli.api.cleanup_policy.collection.CleanupPolicyCollection`
        . This will automatically use the existing instance of
        :class:`NexusClient` to communicate with the Nexus service.
        """
        if self._cleanup_policies is None:
            self._cleanup_policies = CleanupPolicyCollection(client=self)
        return self._cleanup_policies

    @property
    def scripts(self) -> ScriptCollection:
        """
        Instance of
        :class:`~nexuscli.api.script.model.ScriptCollection`. This will
        automatically use the existing instance of :class:`NexusClient` to
        communicate with the Nexus service.
        """
        if self._scripts is None:
            self._scripts = ScriptCollection(client=self)
        return self._scripts

    @property
    def rest_url(self) -> str:
        """
        Full URL to the Nexus REST API, based on the ``url`` and ``version``
        from :attr:`config`.

        :rtype: str
        """
        return urljoin(self.config.url, 'service/rest/')

    @property
    def service_url(self) -> str:
        """
        Full URL to the Nexus REST API, based on the ``url`` and ``version``
        from :attr:`config`.

        :rtype: str
        """
        return urljoin(self.rest_url, self.config.api_version + '/')

    def http_request(
            self, method: str, endpoint: str, service_url: Optional[str] = None,
            **kwargs) -> requests.Response:
        """
        Performs a HTTP request to the Nexus REST API on the specified
        endpoint.

        :param method: one of ``get``, ``put``, ``post``, ``delete``.
        :param endpoint: URI path to be appended to the service URL.
        :param service_url: override the default URL to use for the request,
            which is created by joining :attr:`rest_url` and ``endpoint``.
        :param kwargs: as per :py:func:`requests.request`.
        """
        service_url = service_url or self.service_url
        url = urljoin(service_url, endpoint)

        try:
            response = requests.request(
                method=method, auth=self.config.auth, url=url,
                verify=self.config.x509_verify, **kwargs)
        except requests.exceptions.ConnectionError as e:
            raise exception.NexusClientConnectionError(str(e)) from None

        if response.status_code == 401:
            raise exception.NexusClientInvalidCredentials('Try running `nexus3 login`')

        return response

    def http_get(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Performs a HTTP GET request on the given endpoint.

        :param endpoint: name of the Nexus REST API endpoint.
        """
        return self.http_request('get', endpoint, stream=True, **kwargs)

    def http_head(self, endpoint: str) -> requests.Response:
        """
        Performs a HTTP HEAD request on the given endpoint.

        :param endpoint: name of the Nexus REST API endpoint.
        """
        return self.http_request('head', endpoint)

    def _get_paginated(self, endpoint: str, **request_kwargs) -> Iterator[Dict]:
        """
        Performs a GET request using the given args and kwargs. If the response
        is paginated, the method will repeat the request, manipulating the
        `params` keyword argument each time in order to receive all pages of
        the response.

        Items in the responses are sent in "batches": when all elements of a
        response have been yielded, a new request is made and the process
        repeated.

        :param request_kwargs: passed verbatim to the _request() method, except
            for the argument needed to paginate requests.
        :return: a generator that yields on response item at a time.
        """
        response = self.http_request('get', endpoint, **request_kwargs)
        if response.status_code == 404:
            raise exception.NexusClientAPIError(response.reason)

        try:
            content = response.json()
        except json.decoder.JSONDecodeError:
            raise exception.NexusClientAPIError(response.content)

        while True:
            for item in content.get('items'):
                yield item

            continuation_token = content.get('continuationToken')
            if continuation_token is None:
                break

            request_kwargs['params'].update(
                {'continuationToken': continuation_token})
            response = self.http_request('get', endpoint, **request_kwargs)

            try:
                content = response.json()
            except json.decoder.JSONDecodeError:
                raise exception.NexusClientAPIError(response.content)

    def http_post(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Performs a HTTP POST request on the given endpoint.

        :param endpoint: name of the Nexus REST API endpoint.
        :param kwargs: as per :py:func:`requests.request`.
        """
        return self.http_request('post', endpoint, **kwargs)

    def http_put(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Performs a HTTP PUT request on the given endpoint.

        :param endpoint: name of the Nexus REST API endpoint.
        :param kwargs: as per :py:func:`requests.request`.
        """
        return self.http_request('put', endpoint, **kwargs)

    def http_delete(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Performs a HTTP DELETE request on the given endpoint.

        :param endpoint: name of the Nexus REST API endpoint.
        :param kwargs: as per :py:func:`requests.request`.
        """
        return self.http_request('delete', endpoint, **kwargs)

    def list(self, repository_path: str) -> Iterator[Optional[str]]:
        """
        List all the artefacts, recursively, in a given ``repository_path``.

        :param repository_path: location on the repository service.
        :return: artefacts under ``repository_path``.
        """
        for artefact in self.list_raw(repository_path):
            yield artefact.get('path')

    def _list_raw_search(
            self, repository_name: str, path_filter: str, partial_match: bool) -> Iterator[Dict]:
        # TODO: use `group` attribute in raw repositories to speed-up queries
        query = {
            'repository': repository_name,
        }

        if path_filter:
            query['keyword'] = f'"{path_filter}"'  # hacky as fuck :(

        raw_response = self._get_paginated('search/assets', params=query)

        # TODO: maybe this filter is no longer needed due to keyword use ^
        return nexus_util.filtered_list_gen(
            raw_response, term=path_filter, partial_match=partial_match)

    def list_raw(self, repository_path: str) -> Iterator[Dict]:
        """
        As per :meth:`list` but yields raw Nexus artefacts as dicts.

        :param repository_path: location on the repository service.
        """
        repo, directory, filename = nexus_util.split_component_path(repository_path)
        path_filter = ''  # matches everything
        partial_match = True

        if directory is not None:
            path_filter = directory
            # Not all repos require a directory as part of the artefact path.
            if not (path_filter == '' or
                    path_filter.endswith(Repository.REMOTE_PATH_SEPARATOR)):
                path_filter += Repository.REMOTE_PATH_SEPARATOR

        if filename is not None:
            partial_match = False
            # The artefact path is always relative to the given repo.
            path_filter += filename

        list_gen = self._list_raw_search(repo, path_filter, partial_match)

        for artefact in list_gen:
            yield artefact

    def _upload_dir_or_file(self, file_or_dir, dst_repo, dst_dir, dst_file,
                            **kwargs):
        """
        Helper for self.upload() to call the correct upload method according to
        the source given by the user.

        :param file_or_dir: location or file or directory to be uploaded.
        :param dst_repo: destination repository in Nexus.
        :param dst_dir: destination directory in dst_repo.
        :param dst_file: destination file name.
        :return: number of files uploaded.
        """
        repository = self.repositories.get_by_name(dst_repo)

        if os.path.isdir(file_or_dir):
            src_file = file_or_dir
            if dst_file is not None:
                raise exception.NexusClientInvalidRepositoryPath(
                    'Not allowed to upload a directory to a file')

            return repository.upload_directory(src_file, dst_dir, **kwargs)

        src_dir = file_or_dir
        repository.upload_file(src_dir, dst_dir, dst_file)
        return 1

    def upload(self, source, destination, recurse=True, flatten=False):
        """
        Process an upload. The source must be either a local file name or
        directory. The flatten and recurse options are honoured for
        directory uploads.

        The destination must be a valid Nexus 3 repository path, including the
        repository name as the first component of the path.

        :param source: location of file or directory to be uploaded.
        :type source: str
        :param destination: destination path in Nexus, including repository
            name and, if required, directory name (e.g. raw repos require a
            directory).
        :type destination: str
        :param recurse: do not process sub directories for uploads to remote
        :type recurse: bool
        :param flatten: Flatten directory structure by not reproducing local
                        directory structure remotely
        :type flatten: bool
        :return: number of files uploaded.
        """
        repo, directory, filename = nexus_util.split_component_path(destination)
        upload_count = self._upload_dir_or_file(
            source, repo, directory, filename,
            recurse=recurse, flatten=flatten)

        return upload_count

    def _remote_path_to_local(
            self, remote_src, local_dst, flatten, create=True):
        """
        Takes the remote path of an asset (without the repository name), the
        desired destination in the local file system, and creates the fully
        qualified path according to the instance settings.

        If self.flatten is True, the remote_path isn't reproduced locally.

        If the remote is a directory, we'll always assume the destination is
        also a directory, even if it doesn't end with a /.

        :param remote_src: path to the artefact as reported by the artefact
            service (i.e.: the `path` attribute of an asset object).
        :param local_dst: desired location in the local filesystem for the
            remote_path.
        :param create: whether or not to create the local destination file or
            directory.
        :return: the local path to be used.
        """
        # FIXME: use of multiple .. in the local_dst isn't resolved correctly
        remote_isdir = remote_src.endswith(Repository.REMOTE_PATH_SEPARATOR)
        # force destination to be a directory if the remote is a directory
        destination_isdir = (remote_isdir or
                             local_dst.endswith('.') or
                             local_dst.endswith('..') or
                             local_dst.endswith(self._local_sep))
        local_relative = remote_src.replace(Repository.REMOTE_PATH_SEPARATOR, self._local_sep)
        if flatten:
            local_relative = os.path.basename(local_relative)
        # remote=file, destination=file
        if not (remote_isdir or destination_isdir):
            # if files are given, rename the source to match destination
            local_relative_dir = os.path.dirname(local_relative)
            dst_file_name = os.path.basename(local_dst)
            local_dst = os.path.dirname(local_dst)
            if flatten:
                local_relative = dst_file_name
            else:
                local_relative = os.path.join(
                    local_relative_dir, dst_file_name)

        destination_path = pathlib.Path(local_dst)
        local_path = destination_path.joinpath(local_relative)

        if create:
            nexus_util.ensure_exists(local_path, is_dir=remote_isdir)

        return local_path.absolute()

    @staticmethod
    def _should_skip_download(download_url, download_path, artefact, nocache):
        """False when nocache is set or local file is out-of-date"""
        if nocache:
            try:
                LOG.debug('Removing %s because nocache is set\n', download_path)
                os.remove(download_path)
            except FileNotFoundError:
                pass
            return False

        if nexus_util.has_same_hash(artefact, download_path):
            LOG.debug(f'Skipping {download_url} because local copy '
                      f'{download_path} is up-to-date\n')
            return True

        return False

    def download_file(self, download_url, destination):
        """Download an asset from Nexus artefact repository to local
        file system.

        :param download_url: fully-qualified URL to asset being downloaded.
        :type download_url: str
        :param destination: file or directory location to save downloaded
            asset. Must be an existing directory; any exiting file in this
            location will be overwritten.
        :type destination: str
        :return:
        """
        response = self.http_get(download_url)

        if response.status_code != 200:
            sys.stderr.write(response.__dict__)
            raise exception.DownloadError(
                f'Downloading from {download_url}. '
                f'Reason: {response.reason}')

        with open(destination, 'wb') as fd:
            LOG.debug('Writing %s to %s', download_url, destination)
            for chunk in response.iter_content(chunk_size=8192):
                fd.write(chunk)

    def download(self, source, destination, flatten=False, nocache=False):
        """Process a download. The source must be a valid Nexus 3
        repository path, including the repository name as the first component
        of the path.

        The destination must be a local file name or directory.

        If a file name is given as destination, the asset may be renamed. The
        final destination will depend on ``flatten``.

        :param source: location of artefact or directory on the repository
            service.
        :type source: str
        :param destination: path to the local file or directory.
        :type destination: str
        :param flatten: if True, the remote path isn't reproduced locally.
        :type flatten: bool
        :param nocache: if True, force download of a directory or artefact,
                        ignoring an existing local copy. If false, it will not
                        re-download an existing copy if its checksum matches
                        the one in Nexus (as determined by
                        :meth:`nexuscli.nexus_util.has_same_hash`).
        :type nocache: bool
        :return: number of downloaded files.
        :rtype: int
        """
        download_count = 0
        if source.endswith(Repository.REMOTE_PATH_SEPARATOR) and \
                not (destination.endswith('.') or destination.endswith('..')):
            destination += self._local_sep

        artefacts = self.list_raw(source)

        artefacts = progress.bar(
                [a for a in artefacts], label='Downloading')

        for artefact in artefacts:
            download_url = artefact['downloadUrl']
            artefact_path = artefact['path']
            download_path = self._remote_path_to_local(
                artefact_path, destination, flatten)

            if self._should_skip_download(
                    download_url, download_path, artefact, nocache):
                download_count += 1
                continue

            try:
                self.download_file(download_url, download_path)
                download_count += 1
            except exception.DownloadError:
                LOG.warning('Error downloading %s', download_url)
                continue

        return download_count

    def delete(self, repository_path):
        """
        Delete artefacts, recursively if ``repository_path`` is a directory.

        :param repository_path: location on the repository service.
        :type repository_path: str
        :return: number of deleted files. Negative number for errors.
        :rtype: int
        """

        delete_count = 0
        death_row = self.list_raw(repository_path)

        death_row = progress.bar([a for a in death_row], label='Deleting')

        for artefact in death_row:
            id_ = artefact['id']
            artefact_path = artefact['path']

            response = self.http_delete(f'assets/{id_}')
            LOG.info('Deleted: %s (%s)', artefact_path, id_)
            delete_count += 1
            if response.status_code == 404:
                LOG.warning('File disappeared while deleting')
                LOG.debug(response.reason)
            elif response.status_code != 204:
                LOG.error(response.reason)
                return -1

        return delete_count
