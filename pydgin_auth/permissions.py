''' Module to handle permissions..Permissions should be granted via the admin interface'''
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, User
import logging
from django.shortcuts import get_object_or_404
from elastic.elastic_settings import ElasticSettings
from pydgin_auth.admin import ElasticPermissionModelFactory
logger = logging.getLogger(__name__)


def get_authenticated_idx_and_idx_types(user, idx_keys, idx_type_keys=None):
    ''' Check permissions on elastic indexes and returns indexes that the given user can see'''
    logger.debug('Before permission check idx ' + str(idx_keys))
    logger.debug('Before permission check idx types' + str(idx_type_keys))
    logger.debug(user)

    idx_keys_auth = []
    idx_type_keys_auth = []

    model_names = get_elastic_model_names(idx_keys, idx_type_keys)

    if 'IDX' in model_names:
        model_name_idx = [idx_v for idx_k, idx_v in model_names['IDX'].items() if idx_k in idx_keys]
        idx_names_auth = _check_content_type_perms(model_name_idx, user)
        idx_keys_auth = [idx_k for idx_k, idx_v in model_names['IDX'].items() if idx_v in idx_names_auth]

    if idx_type_keys and 'IDX_TYPE' in model_names:
        model_type_idx = [idx_v for idx_k, idx_v in model_names['IDX_TYPE'].items() if idx_k in idx_type_keys]
        idx_types_auth = _check_content_type_perms(model_type_idx, user)
        idx_type_keys_auth = [idx_k for idx_k, idx_v in model_names['IDX_TYPE'].items()
                              if idx_v in idx_types_auth and idx_k.split('.')[0] in idx_keys_auth]

    logger.debug('After permission check-name' + str(idx_keys_auth))
    logger.debug('After permission check-type' + str(idx_type_keys_auth))

    return (idx_keys_auth, idx_type_keys_auth)


def get_elastic_model_names(idx_keys, idx_type_keys):
    model_names = {}
    model_names['IDX'] = {}
    model_names['IDX_TYPE'] = {}

    elastic_dict = ElasticSettings.attrs().get('IDX')

    for idx_key in idx_keys:
        if idx_key in elastic_dict:
            model_name = idx_key.lower() + ElasticPermissionModelFactory.PERMISSION_MODEL_SUFFIX
            if idx_key not in model_names:
                model_names['IDX'][idx_key] = model_name

            if 'idx_type' in elastic_dict[idx_key] and idx_type_keys is not None:
                idx_type_dict = elastic_dict[idx_key]['idx_type']

                for idx_idx_type in idx_type_keys:
                    if idx_idx_type.startswith(idx_key):
                        idx_type = idx_type_dict[idx_idx_type.partition('.')[2]]['type']

                        model_name = idx_key.lower() + \
                            ElasticPermissionModelFactory.PERMISSION_MODEL_NAME_TYPE_DELIMITER + \
                            idx_type.lower() + ElasticPermissionModelFactory.PERMISSION_MODEL_TYPE_SUFFIX

                        model_names['IDX_TYPE'][idx_idx_type] = model_name

    return model_names


def _check_content_type_perms(idx_names, user):
    ''' Fetch content type and apply it as filter to Permission models,
     and check if the user has perm to see the code_name'''
    idx_names_auth = []
    for idx in idx_names:
        app_name = ElasticPermissionModelFactory.PERMISSION_MODEL_APP_NAME
        model_name = idx
        content_type = None
        try:
            content_type = ContentType.objects.get(model=model_name, app_label=app_name)
        except:
            logger.debug('Content type not found for ' + str(content_type))

        permissions = None
        if content_type:
            permissions = Permission.objects.filter(content_type=content_type)

            if permissions:
                if user is not None and user.is_authenticated():
                    for perm in permissions:
                        perm_code_name = app_name + '.' + perm.codename
                        if user.has_perm(perm_code_name):
                            idx_names_auth.append(idx)
            else:
                idx_names_auth.append(idx)

    return idx_names_auth


def get_user_groups(user):
    '''Get all users in a given group'''
    current_user = get_object_or_404(User, pk=user.id)
    current_user_groups = []
    user_groups = current_user.groups.all()
    for group in user_groups:
        current_user_groups.append(group.name)

    return current_user_groups
