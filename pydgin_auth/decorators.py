'''
Custom decorators using django's decorators
Just to show sample implementation
'''

# from django.contrib.auth.decorators import user_passes_test
# from django.contrib.auth.decorators import permission_required


'''
Decorator Usage:
@user_passes_test(email_check,login_url='/accounts/login/')
def my_view(request):
'''


def email_check(user):
    return user.email.endswith('@example.com')

'''
class Task(models.Model):
    ...
    class Meta:
        permissions = (
            ("view_task", "Can see available tasks"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )
In template
 {% if perms.foo.can_vote %}
        <p>You can vote!</p>
    {% endif %}


In view
@permission_required('polls.can_vote')
def my_view(request):

As for the has_perm() method, permission names take the form "<app label>.<permission codename>"
(i.e. polls.can_vote for a permission on a model in the polls application).

'''
