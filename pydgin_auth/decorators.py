'''
Custom decorators using django's decorators
Just to show sample implementation
'''

from django.contrib.auth.decorators import user_passes_test
# from django.contrib.auth.decorators import permission_required


'''
Decorator Usage:
@user_passes_test(email_check_is_internal,login_url='/accounts/login/')
def my_view(request):
'''


def email_check_is_internal(user):
    return user.email.endswith('cam.ac.uk')


def is_in_group(*group_names, login_url='/accounts/permission_denied/'):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='/accounts/permission_denied/')
