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

import logging
from pydgin_auth.elastic_model_factory import ElasticPermissionModelFactory
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

# call to create elastic models based on the elastic settings
ElasticPermissionModelFactory.create_dynamic_models()
