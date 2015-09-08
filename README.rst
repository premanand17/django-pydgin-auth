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

5. Create users and databases

5.1 Run the following psql commands to create user and dbs.
	sudo -u postgres psql -c "CREATE USER webuser WITH PASSWORD 'webuser';"
	sudo -u postgres psql -c "ALTER USER webuser CREATEDB;"
	
	sudo -u postgres psql -c "CREATE database pydgin_authdb;"
	sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE 'pydgin_coredb' TO webuser;"
	
	sudo -u postgres psql -c "CREATE database pydgin_coredb;"
	sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE 'pydgin_authdb' TO webuser;"



6. How to run migrations?

	6.1 Clear migrations if you already have created them:
		rm -rf python-env/pydgin-env/lib/python3.4/site-packages/django/contrib/auth/migrations/
		rm -rf python-env/pydgin-env/lib/python3.4/site-packages/django/contrib/admin/migrations/
		rm -rf python-env/pydgin-env/lib/python3.4/site-packages/django/contrib/contenttypes/migrations/
		rm -rf python-env/pydgin-env/lib/python3.4/site-packages/django/contrib/sessions/migrations/
		
		rm -rf /gdxbase/www/xxx-dev/django-pydgin-auth/pydgin_auth/migrations/
		rm -rf /gdxbase/www/xxx-dev/python-env/pydgin-env/lib/python3.4/site-packages/rest_framework/authtoken/migrations
		rm -rf /gdxbase/www/xxx-dev/django-elastic/elastic/
		rm -rf /gdxbase/www/xxx-dev/pydgin/pydgin/local_apps/auth_test/migrations

6.2 Make migrations:

		./manage.py makemigrations admin
		./manage.py makemigrations auth
		./manage.py makemigrations contenttypes
		./manage.py makemigrations sessions
		./manage.py makemigrations authtoken
		./manage.py makemigrations pydgin_auth
		./manage.py makemigrations auth_test

6.3 Migrate in the following order:
		
		./manage.py migrate admin --database=pydgin_authdb
		./manage.py migrate contenttypes --database=pydgin_authdb #will be called by admin
		./manage.py migrate auth --database=pydgin_authdb  #will be called by admin
		./manage.py migrate sessions --database=pydgin_authdb
		./manage.py migrate authtoken --database=pydgin_authdb
		./manage.py migrate pydgin_auth --database=pydgin_authdb
		./manage.py migrate auth_test --database=pydgin_authdb
		
		./manage.py makemigrations elastic
		./manage.py migrate elastic --database=pydgin_authdb
		./manage.py migrate  --database=default

6.4 Import test usernames and permissions:

		psql webuser -h localhost -d pydgin_authdb -f pydgin_auth/static/pydgin_auth/data/pydgin_authdb_data.sql


7. Tests can be run as follows::

	    ./manage.py test pydgin_auth.tests 

