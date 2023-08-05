DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

CACHES = {
    "default": {
        # This cache backend is OK to use in development and testing
        # but has the potential to break production setups with more than on process
        # due to each process having their own local memory based cache
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache"
    }
}

SITE_ID = 1

MIDDLEWARE = [
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "dynaperms.backends.DynamicBackend",
    "django.contrib.auth.backends.ModelBackend",
]


ROOT_URLCONF = ""

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.admin",
    "dynaperms",
]

SECRET_KEY = "too-secret-for-test"

USE_I18N = False

USE_L10N = False

USE_TZ = False
