'''
Module to create elastic models dynamically
'''
from django.contrib import admin
from django.contrib.auth.models import Permission

from django.db import models
from django.contrib.contenttypes.models import ContentType
from elastic.elastic_settings import ElasticSettings

from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

import logging
from django.db import connections
from django.conf import settings

logger = logging.getLogger(__name__)


def create_elastic_index_model_manager(model_name, application_label, content_type_id):
    '''
    function to create proxy Model Managers for a given Model
    A Manager is the interface through which database query operations are provided to Django models
    '''
    className = model_name.title() + 'Manager'

    class Meta:
        proxy = True
        verbose_name = className
        app_label = application_label

    model_manager = type(className, (models.Manager, ), {'__module__': 'elastic.models',
                                                         'Meta': Meta, 'cid': content_type_id})

    def get_queryset(self):
        return super(model_manager, self).get_queryset().filter(content_type_id=self.cid)

    setattr(model_manager, 'cid', content_type_id)
    setattr(model_manager, 'get_queryset', get_queryset)
    return model_manager


def create_elastic_index_model(model_name, application_label):
    '''
    function to create proxy Models dynamically.
    Create ContentType and pass the id to the function that creates model manager
    '''

    class Meta:
        proxy = True
        verbose_name = model_name.lower()
        app_label = application_label

    ct, created = ContentType.objects.get_or_create(model=Meta.verbose_name,  # @UnusedVariable
                                                    app_label=Meta.app_label)

    # create permission
    can_read_permission, create = Permission.objects.get_or_create(  # @UnusedVariable
        codename='can_read_' + Meta.verbose_name.lower(),
        name='Can Read ' + Meta.verbose_name.lower(),
        content_type=ct)

    model_manager = create_elastic_index_model_manager(model_name, application_label, ct.id)

    attrs = {'__module__': 'elastic.models', 'Meta': Meta, 'objects': model_manager()}
    elasticmodel = type(model_name, (Permission,), attrs)
    setattr(elasticmodel, 'cid', ct.id)
    setattr(elasticmodel, 'objects', model_manager())
    return elasticmodel, created


class ElasticPermissionModelFactory():
    '''class to create dynamic proxy models and managers for elastic indexes'''
    PERMISSION_MODEL_SUFFIX = '_idx'
    PERMISSION_MODEL_TYPE_SUFFIX = '_idx_type'
    PERMISSION_MODEL_NAME_TYPE_DELIMITER = '-'
    PERMISSION_MODEL_APP_NAME = settings.ELASTIC_PERMISSION_MODEL_APP_NAME

    @classmethod
    def create_dynamic_models(cls):
        '''main function that delegates the call to create the proxy models and managers for elastic indexes'''
        (model_names_idx, model_names_idx_types) = cls.get_elastic_model_names()

        model_names = model_names_idx + model_names_idx_types

        connection = connections[settings.AUTH_DB]
        if "django_content_type" in connection.introspection.table_names():
            for model_name in model_names:
                elasticmodel, created = create_elastic_index_model(model_name,  # @UnusedVariable
                                                                   cls.PERMISSION_MODEL_APP_NAME)

            cls.autoregister()

    @classmethod
    def autoregister(cls, app_label=PERMISSION_MODEL_APP_NAME):
        '''auto register all the models belonging to the given app eg: elastic'''
        for model_ct in ContentType.objects.filter(app_label=app_label):
            print('Model names : ' + model_ct.model)
            model = None
            try:
                model = apps.get_model(app_label=app_label, model_name=model_ct.model.lower())
            except LookupError:
                '''
                If you are here, then content type exists, and model doesn't exists
                Means, you have changed an idx from private to public
                '''
                logger.warn('Model not found for ' + model_ct.model.lower())
                model_name = model_ct.model.lower()
                model, created = create_elastic_index_model(model_name,  # @UnusedVariable
                                                            cls.PERMISSION_MODEL_APP_NAME)
            except:
                pass

            try:
                if model is not None:
                    admin.site.register(model)
            except AlreadyRegistered:
                pass

    @classmethod
    def get_idx_and_idx_type_keys(cls, elastic_dict=None, auth_public=False):
        '''
        Returns the idx and idx type keys
        Use the auth_public flag to restrict to either public or private idx and idx_types
        '''
        if elastic_dict is None:
            elastic_dict = ElasticSettings.attrs().get('IDX')

        idx_type_keys_public = []
        idx_type_keys_private = []

        # get private idx_keys if auth_public is False and public idx_keys otherwise
        idx_keys_public = [idx_key for (idx_key, idx_values) in elastic_dict.items()
                           if('auth_public' in idx_values and idx_values['auth_public'] is True)]
        idx_keys_private = [idx_key for (idx_key, idx_values) in elastic_dict.items()
                            if('auth_public' not in idx_values or idx_values['auth_public'] is False)]

        # get idx_type_keys
        for idx_key in idx_keys_public + idx_keys_private:
            if 'idx_type' in elastic_dict[idx_key]:
                for (idx_type_key, idx_type_values) in elastic_dict[idx_key]['idx_type'].items():

                    if 'auth_public' in idx_type_values and idx_type_values['auth_public'] is True:
                        idx_type_keys_public.append(idx_key + '.' + idx_type_key)

                    if 'auth_public' not in idx_type_values or idx_type_values['auth_public'] is False:
                        idx_type_keys_private.append(idx_key + '.' + idx_type_key)

        # logger.debug('**********PUBLIC IDX and IDX TYPES**************')
        # logger.debug(idx_keys_public)
        # logger.debug(idx_type_keys_public)
        # logger.debug('**********PRIVATE IDX and IDX TYPES**************')
        # logger.debug(idx_keys_private)
        # logger.debug(idx_type_keys_private)

        if auth_public:
            # make case insensitive
            idx_keys_public_icase = [x.upper() for x in idx_keys_public]
            idx_type_keys_public_icase = [x.upper() for x in idx_type_keys_public]
            return idx_keys_public_icase, idx_type_keys_public_icase
        else:
            # make case insensitive
            idx_keys_private_icase = [x.upper() for x in idx_keys_private]
            idx_type_keys_private_icase = [x.upper() for x in idx_type_keys_private]
            return idx_keys_private_icase, idx_type_keys_private_icase

    @classmethod
    def get_elastic_model_names(cls, elastic_dict=None, idx_keys=None, idx_type_keys=None, auth_public=False):
        '''Returns the model names to be created for dynamic models
        Right suffix is added to different the model types'''

        # generate models only for private idx and idx_types
        if idx_keys is None and idx_type_keys is None:
            (idx_keys, idx_type_keys) = cls.get_idx_and_idx_type_keys(elastic_dict=elastic_dict, auth_public=False)

        model_names_idx = [idx_key + ElasticPermissionModelFactory.PERMISSION_MODEL_SUFFIX for idx_key in idx_keys]

        model_names_idx_types = []
        for idx_type_key in idx_type_keys:
            idx_type_key = idx_type_key.replace('.', cls.PERMISSION_MODEL_NAME_TYPE_DELIMITER)
            model_name = idx_type_key + cls.PERMISSION_MODEL_TYPE_SUFFIX
            model_names_idx_types.append(model_name)

        # make case insensitive
        model_names_idx_icase = [model_name.lower() for model_name in model_names_idx]
        model_names_idx_types_icase = [model_name_type.lower() for model_name_type in model_names_idx_types]
        return model_names_idx_icase, model_names_idx_types_icase

    @classmethod
    def get_keys_from_model_names(cls, idx_model_names=None, idx_type_model_names=None):
        '''Returns the idx keys and idx type keys given idx and idx type model names'''

        idx_keys = [model_name.replace(ElasticPermissionModelFactory.PERMISSION_MODEL_SUFFIX,
                                       '') for model_name in idx_model_names]

        idx_type_keys = [model_name.replace(cls.PERMISSION_MODEL_TYPE_SUFFIX,
                                            '').replace(cls.PERMISSION_MODEL_NAME_TYPE_DELIMITER, '.')
                         for model_name in idx_type_model_names]

        # make case insensitive
        idx_keys_icase = [x.upper() for x in idx_keys]
        idx_type_keys_icase = [x.upper() for x in idx_type_keys]
        return(idx_keys_icase, idx_type_keys_icase)

    @classmethod
    def get_db_models(cls, app_label=PERMISSION_MODEL_APP_NAME, existing=False):
        '''Gets the models from settings file and compares with existing elastic models from db.
           Returns only the model that does not exist in db'''
        (model_names_idx, model_names_idx_types) = cls.get_elastic_model_names()
        settings_model_names = model_names_idx + model_names_idx_types

        all_existing_models = ContentType.objects.filter(app_label=app_label)
        all_existing_model_names = [model.name for model in all_existing_models]

        all_non_existing_models = [model for model in settings_model_names if model not in all_existing_model_names]

        if existing:
            return all_existing_model_names
        else:
            return all_non_existing_models
