import inspect
import json

import semver
import sys

from nexuscli import exception
from nexuscli.api import util
from nexuscli.api.base_collection import BaseCollection
from nexuscli.api.repository import model, Repository

# TODO: determine `SCRIPT_CREATE_VERSIONS` based on the existence of a versioned .groovy script
SCRIPT_CREATE_VERSIONS = [semver.VersionInfo(3, 21, 0)]
SCRIPT_NAME_CREATE = 'nexus3-cli-repository-create'
SCRIPT_NAME_DELETE = 'nexus3-cli-repository-delete'
SCRIPT_NAME_GET = 'nexus3-cli-repository-get'


def get_repository_classes():
    members = inspect.getmembers(sys.modules['nexuscli.api.repository.model'], inspect.isclass)
    return [cls for _, cls in members if issubclass(cls, Repository) and cls.DEFAULT_RECIPE]


def get_classes_by_type(repo_types):
    if isinstance(repo_types, str):
        repo_types = [repo_types]

    return [x for x in get_repository_classes() if x.TYPE in repo_types]


def get_recipes_by_type(repo_type):
    return [x.RECIPE_NAME for x in get_classes_by_type(repo_type)]


def get_supported_recipes():
    return sorted(set([cls.DEFAULT_RECIPE for cls in get_repository_classes()]))


def get_repository_class(raw_configuration):
    """
    Given a raw repository configuration, returns its corresponding class.

    :param raw_configuration: configuration as returned by the SCRIPT_NAME_GET
        groovy script.
    :type raw_configuration: dict
    :return: repository class
    """
    recipe_name = _recipe_name(raw_configuration).lower()
    recipe_type = _recipe_type(raw_configuration).lower()
    for class_ in get_classes_by_type(recipe_type):
        if class_.DEFAULT_RECIPE == recipe_name:
            return class_

    raise NotImplementedError(f'{recipe_name} {recipe_type} for {raw_configuration}')


def _recipe_name(raw_configuration):
    """
    Given a raw repository configuration, returns its recipe name.

    :param raw_configuration: configuration as returned by the SCRIPT_NAME_GET
        groovy script.
    :type raw_configuration: dict
    :return: name of the recipe ("format")
    """
    name = raw_configuration['recipeName'].split('-')[0].title()

    if name == 'Maven2':
        name = 'Maven'

    return name


def _recipe_type(raw_configuration):
    """
    Given a raw repository configuration, returns its recipe type.

    :param raw_configuration: configuration as returned by the SCRIPT_NAME_GET
        groovy script.
    :type raw_configuration: dict
    :return: Group, Proxy or Hosted
    """
    return raw_configuration['recipeName'].split('-')[1].title()


# TODO: flattening-out the configuration on the python class turned-out to be
#   a bad idea because now we need to convert it back and forth. Perhaps add
#   a compatible change that allows one to provide the flat kwargs OR a
#   configuration dict in the format accepted/returned by Nexus.
def _add_proxy_kwargs(kwargs, attributes):
    kwargs['auto_block'] = attributes['httpclient']['autoBlock']

    kwargs['content_max_age'] = int(attributes['proxy']['contentMaxAge'])
    kwargs['metadata_max_age'] = int(attributes['proxy']['metadataMaxAge'])
    kwargs['remote_url'] = attributes['proxy']['remoteUrl']

    kwargs['negative_cache_enabled'] = attributes['negativeCache']['enabled']
    kwargs['negative_cache_ttl'] = int(
        attributes['negativeCache']['timeToLive'])


def _add_maven_kwargs(kwargs, attributes):
    kwargs['layout_policy'] = attributes['maven']['layoutPolicy']
    kwargs['version_policy'] = attributes['maven']['versionPolicy']


def _add_yum_kwargs(kwargs, attributes):
    kwargs['depth'] = int(attributes['yum']['repodataDepth'])
    # TODO: support yum deploy policy
    # kwargs['TODO'] = attributes['yum']['deployPolicy']


def _add_apt_kwargs(kwargs, attributes):
    if 'aptSigning' in attributes:
        kwargs['passphrase'] = attributes['aptSigning']['passphrase']
        kwargs['gpg_keypair'] = attributes['aptSigning']['keypair']
    if 'apt' in attributes:
        kwargs['distribution'] = attributes['apt']['distribution']
        if attributes['apt'].get('flat') is not None:
            kwargs['flat'] = attributes['apt']['flat']


def _add_group_kwargs(kwargs, attributes):
    kwargs['member_names'] = attributes['group']['memberNames']


def _add_hosted_kwargs(kwargs, attributes):
    kwargs['write_policy'] = attributes['storage']['writePolicy']


def _add_common_kwargs(kwargs, attributes):
    kwargs['cleanup_policy'] = attributes.get('cleanup', {}).get('policyName')
    if kwargs['cleanup_policy'] == 'None':
        kwargs['cleanup_policy'] = None

    kwargs['blob_store_name'] = attributes['storage']['blobStoreName']
    kwargs['strict_content_type_validation'] = attributes[
        'storage']['strictContentTypeValidation']


def _repository_args_kwargs(raw_configuration):
    args = (raw_configuration['repositoryName'],)
    kwargs = {'recipe': _recipe_name(raw_configuration)}

    attributes = raw_configuration['attributes']
    _add_common_kwargs(kwargs, attributes)

    if _recipe_name(raw_configuration) == 'Maven':
        _add_maven_kwargs(kwargs, attributes)

    if _recipe_name(raw_configuration) == 'Yum':
        _add_yum_kwargs(kwargs, attributes)

    if _recipe_name(raw_configuration) == 'Apt':
        _add_apt_kwargs(kwargs, attributes)

    # TODO: support Group
    if _recipe_type(raw_configuration) == 'Proxy':
        _add_proxy_kwargs(kwargs, attributes)
    elif _recipe_type(raw_configuration) == 'Hosted':
        _add_hosted_kwargs(kwargs, attributes)
    elif _recipe_type(raw_configuration) == 'Group':
        _add_group_kwargs(kwargs, attributes)

    return args, kwargs


class RepositoryCollection(BaseCollection):
    """A class to manage Nexus 3 repositories."""
    def __init__(self, client=None):
        super().__init__(client=client)
        self._repositories_json = None

    def get_by_name(self, name):
        """
        Get a Nexus 3 repository by its name.

        :param name: name of the repository wanted
        :type name: str
        :rtype: nexuscli.api.repository.model.Repository
        :raise exception.NexusClientInvalidRepository: when a repository with
            the given name isn't found.
        """
        configuration = self.get_raw_by_name(name)
        cls = get_repository_class(configuration)
        args, kwargs = _repository_args_kwargs(configuration)

        return cls(*args, nexus_client=self._client, **kwargs)

    def get_raw_by_name(self, name):
        """
        Return the raw dict for the repository called ``name``. Remember to
        :meth:`refresh` to get the latest from the server.

        :param name: name of the repository wanted
        :type name: str
        :rtype: dict
        :raise exception.NexusClientInvalidRepository: when a repository with
            the given name isn't found.
        """
        self._client.scripts.create_if_missing(SCRIPT_NAME_GET)

        resp = self._client.scripts.run(SCRIPT_NAME_GET, data=name)
        configuration = resp.get('result')

        if configuration == 'null':
            raise exception.NexusClientInvalidRepository(name)

        return json.loads(configuration)

    # TODO: deprecate; replace with reset, as per realms/collection
    def refresh(self):
        """
        Refresh local list of repositories with latest from service. A raw
        representation of repositories can be fetched using :meth:`raw_list`.
        """
        response = self._client.http_get('repositories')
        if response.status_code != 200:
            raise exception.NexusClientAPIError(response.content)

        self._repositories_json = response.json()

    def raw_list(self):
        """
        A raw representation of the Nexus repositories.

        Returns:
            dict: for the format, see `List Repositories
            <https://help.sonatype.com/repomanager3/rest-and-integration-api/repositories-api#RepositoriesAPI-ListRepositories>`_.
        """
        self.refresh()
        return self._repositories_json

    def delete(self, name):
        """
        Delete a repository.

        :param name: name of the repository to be deleted.
        :type name: str
        """
        self._client.scripts.create_if_missing(SCRIPT_NAME_DELETE)
        self._client.scripts.run(SCRIPT_NAME_DELETE, data=name)

    def create(self, repository):
        """
        Creates a Nexus repository with the given format and type.

        :param repository: the instance containing the settings for the
            repository to be created.
        :type repository: Repository
        :raises NexusClientCreateRepositoryError: error creating repository.
        """
        script_name = util.script_for_version(
            SCRIPT_NAME_CREATE,
            self._client.server_version,
            SCRIPT_CREATE_VERSIONS)

        if not issubclass(type(repository), model.Repository):
            raise TypeError(f'{repository} has type {type(repository)}'
                            f' but must be a subclass of Repository')

        self._client.scripts.create_if_missing(script_name)

        script_args = json.dumps(repository.configuration)
        resp = self._client.scripts.run(script_name, data=script_args)

        result = resp.get('result')
        if result != 'null':
            raise exception.NexusClientCreateRepositoryError(resp)

    @util.with_min_version('3.20.1')
    def set_health_check(self, name: str, enable: bool = False) -> None:
        """
        Set the health check status on a Nexus 3 repository.

        :param name: name of the repository wanted
        :param enable: whether to enable of disable the health check
        :rtype: nexuscli.api.repository.model.Repository
        :raise exception.NexusClientInvalidRepository: when a repository with
            the given name isn't found.
        """
        endpoint = f'repositories/{name}/health-check'
        service_url = self._client.rest_url + 'beta/'

        if enable:
            resp = self._client.http_post(endpoint, service_url=service_url, data='')
        else:
            resp = self._client.http_delete(endpoint, service_url=service_url)

        if resp.status_code != 204:
            raise exception.NexusClientAPIError(resp.content)
