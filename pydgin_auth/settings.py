"""
Django settings for pydgin_auth app

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""


LOGIN_REDIRECT_URL = '/'

LOGIN_EXEMPT_URLS = (r'^pydgin_auth',
                     r'^accounts',
                     r'^admin',
                     r'^auth_test/$',
                     r'^$',
                     )
