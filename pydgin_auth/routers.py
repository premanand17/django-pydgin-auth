class AuthRouter(object):
    """
    A router to control database operations on models. We can customize which database to use for which application
    """
    APP_LIST = ('auth', 'admin', 'pydgin_auth', 'contenttypes', 'sessions', 'staticfiles', 'authtoken', 'elastic')

    # remember this is the key of the database definitions in the settings file
    AUTH_DB = 'pydgin_authdb'

    def db_for_read(self, model, **hints):
        """
        Attempts to read pydgin_auth models go to pydgin_authdb.
        """
        if model._meta.app_label in AuthRouter.APP_LIST:
            return AuthRouter.AUTH_DB
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label in AuthRouter.APP_LIST:
            return AuthRouter.AUTH_DB
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label in AuthRouter.APP_LIST or obj2._meta.app_label in AuthRouter.APP_LIST:
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the pydgin_auth app only appears in the 'pydgin_authdb'
        database.
        """
        if app_label in AuthRouter.APP_LIST:
            return db == AuthRouter.AUTH_DB
        return None
