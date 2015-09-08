======
Pydgin-auth
======

Pydgin-auth is a Django app to manage user authentication and authorization. It uses Django’s user authentication system to handle user accounts, groups, permissions, and cookie-based user sessions.

Quick start
-----------

1. Installation::

    pip install -e git://github.com/D-I-L/django-pydgin-auth.git@develop#egg=pydgin-auth


2. If you need to start a Django project:: (skip this if you are adding to existing project)

    django-admin startproject [project_name]

3. Add "pydgin-auth" to your ``INSTALLED_APPS`` in ``settings.py``::

    INSTALLED_APPS = (
        ...
        'pydgin-auth',
        'auth_test'
    )

4. Add the following lines to your project settings.py::

	AUTH_PROFILE_MODULE = "pydgin_auth.UserProfile"
	# Import Applicaton-specific Settings
	PYDGIN_AUTH_APPS_BASE_NAME = 'pydgin_auth'
	for app in INSTALLED_APPS:
	    if app.startswith(PYDGIN_AUTH_APPS_BASE_NAME):
	        try:
	            app_module = __import__(app, globals(), locals(), ["settings"])
	            app_settings = getattr(app_module, "settings", None)
	            for setting in dir(app_settings):
	                if setting == setting.upper():
	                    locals()[setting] = getattr(app_settings, setting)
	        except ImportError:
	            pass

5. Create users and databases::

	sudo -u postgres psql -c "CREATE USER webuser WITH PASSWORD 'webuser';"
	sudo -u postgres psql -c "ALTER USER webuser CREATEDB;"
	
	sudo -u postgres psql -c "CREATE database pydgin_authdb;"
	sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE "pydgin_authdb" TO webuser;"
	
	sudo -u postgres psql -c "CREATE database pydgin_coredb;"
	sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE "pydgin_coredb" TO webuser;"


6. Migrations - Clear migrations if you already have created them::
	
	find /gdxbase/www/xxx-dev/python-env/[VIRTUAL_ENV]/lib/python3.4/site-packages/ -name "000*" -exec rm -rf {} \; 
	
7. Migrations - Makemigrations::

	./manage.py makemigrations admin
	./manage.py makemigrations auth
	./manage.py makemigrations contenttypes
	./manage.py makemigrations sessions
	./manage.py makemigrations authtoken
	./manage.py makemigrations pydgin_auth
	./manage.py makemigrations auth_test

8. Migrations - Migrate in the following order::

	./manage.py migrate admin --database=pydgin_authdb
	./manage.py migrate sessions --database=pydgin_authdb
	./manage.py migrate authtoken --database=pydgin_authdb
	./manage.py migrate pydgin_auth --database=pydgin_authdb
	./manage.py migrate auth_test --database=pydgin_authdb
		
	./manage.py makemigrations elastic
	./manage.py migrate elastic --database=pydgin_authdb
	./manage.py migrate  --database=default

9. Import test usernames and permissions::

	psql webuser -h localhost -d pydgin_authdb -f ../django-pydgin-auth/pydgin_auth/static/pydgin_auth/data/pydgin_authdb_data.sql
	(Note: password is webuser)

10. Run the server::
	./manage runserver xxxx-rh1:8000
	
11. Tests can be run as follows::

	./manage.py test pydgin_auth.tests 

12. Test site::
	Viist site http://xxxx-rh1:8000/
	Login and try to access auth_test home at  http://xxxx-rh1:8000/auth_test/
	