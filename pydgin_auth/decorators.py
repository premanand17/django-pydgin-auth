'''
Custom decorators using django's decorators
Just to show sample implementation
'''

# from django.contrib.auth.decorators import user_passes_test
# from django.contrib.auth.decorators import permission_required


'''
Decorator Usage:
@user_passes_test(email_check_is_internal,login_url='/accounts/login/')
def my_view(request):
'''


def email_check_is_internal(user):
    return user.email.endswith('cam.ac.uk')
