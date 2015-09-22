'''
Module to create elastic models dynamically
'''
from django.contrib import admin
from django.contrib.auth.models import Permission

from django.db import models
from django.contrib.contenttypes.models import ContentType
from elastic.elastic_settings import ElasticSettings
import logging
from django.db import connections
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
        verbose_name = model_name
        app_label = application_label

    ct, created = ContentType.objects.get_or_create(model=Meta.verbose_name,  # @UnusedVariable
                                                    app_label=Meta.app_label)

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
    PERMISSION_MODEL_APP_NAME = 'elastic'

    @classmethod
    def create_dynamic_models(cls):
        '''main function that delegates the call to create the proxy models and managers for elastic indexes'''
        (model_names, model_types) = cls.get_elastic_model_names(as_list=True)
        connection = connections['pydgin_authdb']

        if "django_content_type" in connection.introspection.table_names():
            for model_name in (model_names + model_types):
                elasticmodel, created = create_elastic_index_model(model_name,  # @UnusedVariable
                                                                   cls.PERMISSION_MODEL_APP_NAME)
                admin.site.register(elasticmodel)

    @classmethod
    def get_elastic_model_names(cls, as_list=False):
        '''returns the name of the models assigned to IDX and IDX_TYPES as dict'''

        model_names = {}
        model_names['IDX'] = {}
        model_names['IDX_TYPE'] = {}

        elastic_dict = ElasticSettings.attrs().get('IDX')

        elastic_idx_names = list(elastic_dict.keys())

        for els_idx in elastic_idx_names:
            model_name = els_idx.lower() + cls.PERMISSION_MODEL_SUFFIX

            if els_idx not in model_names:
                model_names['IDX'][els_idx] = model_name

            index_dict = elastic_dict[els_idx]

            if 'search_engine' in index_dict:
                idx_types = list(index_dict['search_engine'])

                for idx_type in idx_types:
                    model_name = els_idx.lower() + cls.PERMISSION_MODEL_NAME_TYPE_DELIMITER + \
                        idx_type.lower() + cls.PERMISSION_MODEL_TYPE_SUFFIX
                    if els_idx in model_names['IDX_TYPE']:
                        idx_types = model_names['IDX_TYPE'][els_idx]
                        idx_types.append(model_name)
                    else:
                        model_names['IDX_TYPE'][els_idx] = [model_name]

        if as_list:
            return cls.get_elastic_model_names_list(model_names)
        else:
            return model_names

    @classmethod
    def get_elastic_model_names_list(cls, model_names_dict):
        '''returns the name of the models to be created based in IDX settings as list'''
        model_names_list = []
        model_types_list = []

        for model_key in model_names_dict['IDX'].keys():
                model_name_idx = model_names_dict['IDX'][model_key]
                model_names_list.append(model_name_idx)
                for model_name_idx_type in list(model_names_dict['IDX_TYPE'][model_key]):
                    model_types_list.append(model_name_idx_type)

        return (model_names_list, model_types_list)
