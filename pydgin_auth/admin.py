'''
Module to customize models in the admin interface.
The ModelAdmin class is the representation of a model in the admin interface.
These are stored in admin.py in your application.
Django finds this module via autodiscovery and executes this everytime when the server is started
'''
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission

from django.db import models
from django.contrib.contenttypes.models import ContentType
from elastic.elastic_settings import ElasticSettings
import logging
logger = logging.getLogger(__name__)

admin.site.site_header = 'PYDGIN USER ADMIN'


def roles(self):
    '''Function to customize the groups in admin interface'''
    p = sorted([u"<a title='%s'>%s</a>" % (x, x) for x in self.groups.all()])
    if self.user_permissions.count():
        p += ['+']
    value = ', '.join(p)
    return mark_safe("<nobr>%s</nobr>" % value)
roles.allow_tags = True
roles.short_description = u'Groups'


def last(self):
    '''Function to format the last login date and fine'''
    fmt = "%b %d, %H:%M"
    value = self.last_login.strftime(fmt)
    return mark_safe("<nobr>%s</nobr>" % value)
last.allow_tags = True
last.admin_order_field = 'last_login'


def adm(self):
    '''return True if user is superuser'''
    return self.is_superuser
adm.boolean = True
adm.admin_order_field = 'is_superuser'


def staff(self):
    '''return True if user is staff'''
    return self.is_staff
staff.boolean = True
staff.admin_order_field = 'is_staff'


def terms_agreed(self):
    '''return True if the user has accepted the terms'''
    return self.profile.is_terms_agreed
terms_agreed.boolean = True
terms_agreed.admin_order_field = 'is_terms_agreed'


def persons(self):
    '''Returns all the users appended by , for a GROUP'''
    return ', '.join(['<a href="%s">%s</a>' % (reverse('admin:auth_user_change', args=(x.id,)), x.username)
                      for x in self.user_set.all().order_by('username')])
persons.allow_tags = True


class UserAdmin(UserAdmin):
    '''ModelAdmin Class to alter the display for Users'''
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', terms_agreed, staff, adm, roles, last]
    list_filter = ['groups', 'is_staff', 'is_superuser', 'is_active']


class GroupAdmin(GroupAdmin):
    '''ModelAdmin Class to alter the display for Groups'''
    list_display = ['name', persons]
    list_display_links = ['name']

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Permission)


# ======================
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

    ct, created = ContentType.objects.get_or_create(model=Meta.verbose_name, app_label=Meta.app_label)
    logger.debug("Status of " + str(Meta.verbose_name) + " is  " + str(created) + ' OBject id is ' + str(ct.id))
    model_manager = create_elastic_index_model_manager(model_name, application_label, ct.id)

    attrs = {'__module__': 'elastic.models', 'Meta': Meta, 'objects': model_manager()}
    elasticmodel = type(model_name, (Permission,), attrs)
    setattr(elasticmodel, 'cid', ct.id)
    setattr(elasticmodel, 'objects', model_manager())
    return elasticmodel


class ElasticPermissionModelFactory():
    '''class to create dynamic proxy models and managers for elastic indexes'''

    PERMISSION_MODEL_SUFFIX = '_elastic_permission'
    PERMISSION_MODEL_APP_NAME = 'elastic'

    idx_names = ElasticSettings.attrs().get('SEARCH').get('IDX_TYPES').keys()
    logger.debug(idx_names)

    elastic_idx = ElasticSettings.attrs().get('SEARCH').get('IDX_TYPES').keys()
    for idx in elastic_idx:
        model_name = idx.lower() + PERMISSION_MODEL_SUFFIX
        elasticmodel = create_elastic_index_model(model_name, PERMISSION_MODEL_APP_NAME)
        admin.site.register(elasticmodel)
