from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission

from django.db import models
from django.contrib.contenttypes.models import ContentType


def roles(self):
    p = sorted([u"<a title='%s'>%s</a>" % (x, x) for x in self.groups.all()])
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


# ======================
def create_elastic_index_model_manager(model_name, content_type_id):
    className = model_name.title() + 'Manager'

    class Meta:
        proxy = True
        verbose_name = className
        app_label = 'elastic'

    model_manager = type(className, (models.Manager, ), {'__module__': 'elastic.models',
                                                         'Meta': Meta, 'cid': content_type_id})

    def get_queryset(self):
        return super(model_manager, self).get_queryset().filter(content_type_id=self.cid)

    setattr(model_manager, 'cid', content_type_id)
    setattr(model_manager, 'get_queryset', get_queryset)
    return model_manager


def create_elastic_index_model(model_name):

    class Meta:
        proxy = True
        verbose_name = model_name
        app_label = 'elastic'

    ct, created = ContentType.objects.get_or_create(model=Meta.verbose_name, app_label=Meta.app_label)
    print("Status of " + str(Meta.verbose_name) + " is  " + str(created) + ' OBject id is ' + str(ct.id))
    model_manager = create_elastic_index_model_manager(model_name, ct.id)

    attrs = {'__module__': 'elastic.models', 'Meta': Meta, 'objects': model_manager()}
    elasticmodel = type(model_name, (Permission,), attrs)
    setattr(elasticmodel, 'cid', ct.id)
    setattr(elasticmodel, 'objects', model_manager())
    return elasticmodel


class ModelFactory():
    print("================CREATING DYNAMIC MODELS FROM ADMIN.PY ModelFactory=================")
    elastic_idx = ['GENE', 'MARKER', 'PUBLICATION']
    for idx in elastic_idx:
        print('Name of index ' + idx)
        model_name = idx.lower() + '_elastic_permission'
        elasticmodel = create_elastic_index_model(model_name)
        admin.site.register(elasticmodel)
