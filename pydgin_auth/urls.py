from django.conf.urls import url
from django.contrib import admin
import django.contrib.auth.views
import pydgin_auth.views
admin.autodiscover()


# Registration URLs
urlpatterns = [url(r'^login/$',  django.contrib.auth.views.login),
               url(r'^logout/$', django.contrib.auth.views.logout, {'next_page': '/human_GRCh38/'}),
               url(r'^profile/$',  pydgin_auth.views.profile),
               url(r'^register/$', pydgin_auth.views.register),
               url(r'^register/complete/$', pydgin_auth.views.registration_complete),
               url(r'^user/password/reset/$', django.contrib.auth.views.password_reset,
                   {'post_reset_redirect': '/accounts/user/password/reset/done/',
                    'template_name': 'registration/admin/password_reset_form.html',
                    'email_template_name': 'registration/admin/password_reset_email.html',
                    'subject_template_name': 'registration/admin/password_reset_subject.txt'},
                   name="password_reset"),
               url(r'^user/password/reset/done/$', django.contrib.auth.views.password_reset_done,
                   {'template_name': 'registration/admin/password_reset_done.html'}),
               url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                   django.contrib.auth.views.password_reset_confirm,
                   {'post_reset_redirect': '/accounts/user/password/done/',
                    'template_name': 'registration/admin/password_reset_confirm.html'},
                   name="password_reset_confirm"),
               url(r'^user/password/done/$', django.contrib.auth.views.password_reset_complete),
               ]
