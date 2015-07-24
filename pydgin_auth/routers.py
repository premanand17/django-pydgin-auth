class AuthRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read pydgin_auth models go to pydgin_authdb.
        """
        app_list = ('auth', 'admin', 'pydgin_auth', 'contenttypes', 'sessions', 'staticfiles', 'authtoken')
        if model._meta.app_label in app_list:
            return 'pydgin_authdb2'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        app_list = ('auth', 'admin', 'pydgin_auth', 'contenttypes', 'sessions', 'staticfiles', 'authtoken')
        # print('Writing models ' + model._meta.app_label)
        if model._meta.app_label in app_list:
            return 'pydgin_authdb2'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        app_list = ('auth', 'admin', 'pydgin_auth', 'contenttypes', 'sessions', 'staticfiles', 'authtoken')
        if obj1._meta.app_label in app_list or obj2._meta.app_label in app_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the pydgin_auth app only appears in the 'pydgin_authdb'
        database.
        """
        app_list = ('auth', 'admin', 'pydgin_auth', 'contenttypes', 'sessions', 'staticfiles', 'authtoken')
        # print('migrating models ' + app_label)
        if app_label in app_list:
            return db == 'pydgin_authdb2'
        return None
