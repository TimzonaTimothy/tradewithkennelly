"""
Django settings for bitcoin project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vwji6*o+^@hs2x&^*h@oxw!pq33x2(i*deue$w_!&#_r)^l8$u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['*','https://tradewithkennellysi.onrender.com',]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'accounts.apps.AccountsConfig',
    'payments',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    # 'accounts.middlewares.SortUserBalance',
]

SESSION_EXPIRE_SECONDS = 12000
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = False
SESSION_TIMEOUT_REDIRECT = '/sign_in'

ROOT_URLCONF = 'bitcoin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bitcoin.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'fundltpr_nextafinance',
#         'USER': 'fundltpr_nextafinance',
#         'PASSWORD': 'nextafinance1',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#         'OPTIONS': {'charset': 'utf8mb4'},
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'mysql.connector.django',
#         'NAME': 'fundltpr_nextafinance',
#         'USER': 'fundltpr_nextafinance',
#         'PASSWORD': 'nextafinance1',
#         'HOST': '127.0.0.1',
#         'PORT': '3306'
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# SECURE_SSL_REDIRECT=True
# SESSION_COOKIE_SECURE=True
# CSRF_COOKIE_SECURE=True



# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'bitcoin/static')
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'arizonatymothy@gmail.com'
EMAIL_HOST_PASSWORD = 'rkzkvluptusfgjtk'
DEFAULT_FROM_EMAIL = "arizonatymothy@gmail.com"
ADMIN_EMAIL = 'arizonatymothy@gmail.com' 


JAZZMIN_SETTINGS = {
    
    "related_modal_active": True,
    "site_logo": "/logo.png",
    "site_icon":  "/logo.png",
    "login_logo": "/logo.png",
    "site_logo_classes": "img-block",
    "site_icon": "/logo.png",
    "welcome_sign": "Welcome to the admin panel",
    "copyright": "grant",
    "search_model": "auth.User",
    "user_avatar": "/img/icons/favicon.png",
     "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user-shield",
        "auth.Group": "fas fa-users",
        "blog.Post": "fas fa-blog",
        "blog.subscribeduser": "fas fa-user-check",
        "blog.Blogcategory": "fas fa-th",
        "Category.category": "fas fa-th",
        "Main.product": "fas fa-list",
    },
    "default_icon_parents": "fas fa-heart",
    "default_icon_children": "fas fa-circle",
    "custom_links": {
    "blogs": [{
        # Any Name you like
        "name": "Make Messages",

        # url name e.g `admin:index`, relative urls e.g `/admin/index` or absolute urls e.g `https://domain.com/admin/index`
        "url": "make_messages",

        # any font-awesome icon, see list here https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2 (optional)
        "icon": "fas fa-comments",

        # a list of permissions the user must have to see this link (optional)
        "permissions": ["books.view_book"]     
    }]
},
    "custom_css": "static/css/main.css",
    "custom_js": "common/js/main.js"
    

    
}

JAZZMIN_SETTINGS["show_ui_builder"] = False

JAZZMIN_UI_TWEAKS = {
    
    "theme": "united",
    # "theme": "flatly",
    # "dark_mode_theme": "darkly",
}