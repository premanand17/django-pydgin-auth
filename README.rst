======
Pydgin-auth
======

Pydgin-auth is a Django app to manage user authentication and authorization. It uses Django’s user authentication system to handle user accounts, groups, permissions, and cookie-based user sessions.

Quick start
-----------

1. Installation::

    pip install -e git://github.com/D-I-L/django-pydgin-auth.git#egg=pydgin-auth


2. If you need to start a Django project::

    django-admin startproject [project_name]

3. Add "pydgin-auth" to your ``INSTALLED_APPS`` in ``settings.py``::

    INSTALLED_APPS = (
        ...
        'pydgin-auth',
    )

4. Add the pydgin-auth settings to the settings.py::

    # pydgin-auth
    PYDGIN-AUTH = {
    }

5. Tests can be run as follows::

    ./manage.py test 

 
