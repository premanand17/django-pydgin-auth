''' Module to handle permissions..Permissions should be granted via the admin interface'''
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, User
import logging
from django.shortcuts import get_object_or_404
logger = logging.getLogger(__name__)
from pydgin_auth.admin import ElasticPermissionModelFactory


def check_index_perms(user, idx_names, idx_types=None):
    ''' Check permissions on elastic indexes and returns indexes that the given user can see'''
    logger.debug('Before permission check idx ' + str(idx_names))
    logger.debug('Before permission check idx types' + str(idx_types))
    logger.debug(user)

    idx_types_auth = []

    idx_names_auth = _check_content_type_perms(idx_names, user)
    idx_names_auth_ori = [idx_name.replace(ElasticPermissionModelFactory.PERMISSION_MODEL_SUFFIX, '')
                          for idx_name in idx_names_auth]

    if idx_types:
        idx_types_filtered = [idx_type for idx_name in idx_names_auth_ori
                              for idx_type in idx_types if idx_type.startswith(idx_name)]
        idx_types_auth = _check_content_type_perms(idx_types_filtered, user)

    logger.debug('After permission check-name' + str(idx_names_auth))
    logger.debug('After permission check-type' + str(idx_types_auth))

    return (idx_names_auth, idx_types_auth)


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


def check_has_permission(user, idx):
    '''Check if the user has any permissions granted on the given model'''
    app_name = ElasticPermissionModelFactory.PERMISSION_MODEL_APP_NAME
    model_name = idx.lower() + ElasticPermissionModelFactory.PERMISSION_MODEL_SUFFIX
    permissions = None

    try:
        content_type = ContentType.objects.get(model=model_name, app_label=app_name)
        permissions = Permission.objects.filter(content_type=content_type)
    except:
        pass

    if permissions:
        if user.is_authenticated():
            for perm in permissions:
                perm_code_name = app_name + '.' + perm.codename
                if user.has_perm(perm_code_name):
                    return True
    else:
        return True

    return False


def get_user_groups(user):
    '''Get all users in a given group'''
    current_user = get_object_or_404(User, pk=user.id)
    current_user_groups = []
    user_groups = current_user.groups.all()
    for group in user_groups:
        current_user_groups.append(group.name)

    return current_user_groups
