import os

from configurations import Configuration, values

from .values import AdminsValue


class BaseDir(object):
    """Provide absolute path to project package root directory as BASE_DIR setting.

    Use it to build your absolute paths like this::

        os.path.join(BaseDir.BASE_DIR, 'templates')
    """

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    NODE_MODULES = os.path.join(os.path.dirname(BASE_DIR), 'node_modules')


class Common(Configuration):
    """Common configuration base class."""

    SECRET_KEY = '(_j4e0=pbe(b+b1$^ch_48be0=gszglcgfzz^dy=(gnx=@m*b7'

    DEBUG = values.BooleanValue(False)

    MAIL_ADMINS = values.BooleanValue(False)

    ADMINS = AdminsValue(
        (('Max Brauer', 'max@max-brauer.de'),)
    )
    MANAGERS = ADMINS

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
            },
            'null': {
                'class': 'logging.NullHandler',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.security': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.security.DisallowedHost': {
                'handlers': ['null'],
                'propagate': False,
            },
            'py.warnings': {
                'handlers': ['console'],
            },
        }
    }

    ALLOWED_HOSTS = values.ListValue(['www.max-brauer.de', 'localhost', '127.0.0.1'])

    SITE_ID = values.IntegerValue(1)

    # Internationalization
    # https://docs.djangoproject.com/en/dev/topics/i18n/
    LANGUAGE_CODE = values.Value('en-us')

    TIME_ZONE = values.Value('Europe/Berlin')

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Absolute filesystem path to the directory that will hold user-uploaded files.
    # Example: "/var/www/example.com/media/"
    MEDIA_ROOT = values.PathValue(os.path.join(BaseDir.BASE_DIR, 'media'))

    # URL that handles the media served from MEDIA_ROOT. Make sure to use a
    # trailing slash.
    # Examples: "http://example.com/media/", "http://media.example.com/"
    MEDIA_URL = values.Value('/media/')

    # Absolute path to the directory static files should be collected to.
    # Don't put anything in this directory yourself; store your static files
    # in apps' "static/" subdirectories and in STATICFILES_DIRS.
    # Example: "/var/www/example.com/static/"
    STATIC_ROOT = values.PathValue(os.path.join(BaseDir.BASE_DIR, 'static_root'))

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/dev/howto/static-files/
    STATIC_URL = values.Value('/static/')

    # Additional locations of static files
    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        os.path.join(BaseDir.BASE_DIR, 'static'),
        BaseDir.NODE_MODULES
    )

    STATICFILES_FINDERS = values.ListValue([
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
        #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
        'sass_processor.finders.CssFinder',
    ])

    MIDDLEWARE_CLASSES = values.ListValue([
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',

        'wagtail.wagtailcore.middleware.SiteMiddleware',
        'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    ])

    ROOT_URLCONF = 'maxbrauer.config.urls'

    WSGI_APPLICATION = 'maxbrauer.config.wsgi.application'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BaseDir.BASE_DIR, 'templates'), ],
            'OPTIONS': {
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ],
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'maxbrauer.context_processors.django_version',
                ],
                'debug': values.BooleanValue(
                    False,
                    environ_name='DJANGO_TEMPLATES_TEMPLATE_DEBUG'
                ),
                'string_if_invalid': values.Value(
                    'INVALID_TEMPLATE_VARIABLE',
                    environ_name='DJANGO_TEMPLATES_STRING_IF_INVALID'
                ),
            },
        },
    ]

    # the following line is only necessary because django-template-debug uses it
    TEMPLATE_DEBUG = TEMPLATES[0]['OPTIONS'].get('debug', False)

    FIXTURE_DIRS = (
        os.path.join(BaseDir.BASE_DIR, 'fixtures'),
    )

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.sitemaps',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'django.contrib.admindocs',
        'crispy_forms',
        'sass_processor',
        'rules.apps.AutodiscoverRulesConfig',

        # wagtail apps
        'wagtail.wagtailforms',
        'wagtail.wagtailredirects',
        'wagtail.wagtailembeds',
        'wagtail.wagtailsites',
        'wagtail.wagtailusers',
        'wagtail.wagtailsnippets',
        'wagtail.wagtaildocs',
        'wagtail.wagtailimages',
        'wagtail.wagtailsearch',
        'wagtail.wagtailadmin',
        'wagtail.wagtailcore',
        "wagtail.contrib.wagtailsitemaps",
        'modelcluster',
        'taggit',

        # wagtail third party
        'blog',

        # custom apps
        'maxbrauer.apps.pages.apps.PagesConfig',
        'maxbrauer.apps.blogutils.apps.BlogUtilsConfig',
    )

    SASS_PROCESSOR_INCLUDE_DIRS = [
        os.path.join(BaseDir.BASE_DIR, 'static/scss'),
        BaseDir.NODE_MODULES,
    ]

    SASS_OUTPUT_STYLE = values.Value('compact')

    SASS_PRECISION = values.IntegerValue(8)

    SASS_PROCESSOR_AUTO_INCLUDE = values.BooleanValue(True)

    CACHES = values. DictValue({
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    })

    EMAIL_SUBJECT_PREFIX = '[max-brauer.de]'

    DEFAULT_FROM_EMAIL = values.EmailValue('max@max-brauer.de')

    SERVER_EMAIL = DEFAULT_FROM_EMAIL

    WAGTAIL_SITE_NAME = "max-brauer.de"

    BLOG_PAGINATION_PER_PAGE = values.IntegerValue(3)
