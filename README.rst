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

    ./manage.py test pydgin_auth 

6. How to run migrations
Run the default migrations
./manage.py makemigrations
./manage.py migrate 

./manage.py makemigrations admin
./manage.py makemigrations auth
./manage.py makemigrations contenttypes
./manage.py makemigrations sessions
./manage.py makemigrations authtoken
./manage.py makemigrations pydgin_auth

./manage.py migrate admin --database=pydgin_authdb
./manage.py migrate contenttypes --database=pydgin_authdb
./manage.py migrate auth --database=pydgin_authdb
./manage.py migrate sessions --database=pydgin_authdb
./manage.py migrate authtoken --database=pydgin_authdb
./manage.py migrate pydgin_auth --database=pydgin_authdb

