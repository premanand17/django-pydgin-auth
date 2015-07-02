from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from requests_oauthlib.oauth1_auth import unicode
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission


def roles(self):
    short_name = unicode  # function to get group name
    # short_name = lambda x: unicode(x)[:1].upper() # first letter of a group
    p = sorted([u"<a title='%s'>%s</a>" % (x, short_name(x)) for x in self.groups.all()])
    if self.user_permissions.count():
        p += ['+']
    value = ', '.join(p)
    return mark_safe("<nobr>%s</nobr>" % value)
roles.allow_tags = True
roles.short_description = u'Groups'


def last(self):
    fmt = "%b %d, %H:%M"
    value = self.last_login.strftime(fmt)
    return mark_safe("<nobr>%s</nobr>" % value)
last.allow_tags = True
last.admin_order_field = 'last_login'


def adm(self):
    return self.is_superuser
adm.boolean = True
adm.admin_order_field = 'is_superuser'


def staff(self):
    return self.is_staff
staff.boolean = True
staff.admin_order_field = 'is_staff'


def persons(self):
    return ', '.join(['<a href="%s">%s</a>' % (reverse('admin:auth_user_change', args=(x.id,)), x.username)
                      for x in self.user_set.all().order_by('username')])
persons.allow_tags = True


class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', staff, adm, roles, last]
    list_filter = ['groups', 'is_staff', 'is_superuser', 'is_active']


class GroupAdmin(GroupAdmin):
    list_display = ['name', persons]
    list_display_links = ['name']

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Permission)
