"""
Django settings for tienda project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--9wyz@2^n^+u7s(+_9^^=_4b)-)hxn-!44m54mfn_og#dpg0a6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['gaudeix.info', 'localhost', '127.0.0.1']

# Application definition
SITE_ID = 1
ANONYMOUS_USER_ID = -1

INSTALLED_APPS = [
    'parler', # idiomas
    'accounts',
    'cart', #carrito
    'djmoney',
    'colorfield',
    'django_ckeditor_5',
    'common',
    'pricing',
    'widget_tweaks',
    'django_countries',
    'django.contrib.sites',
    'allauth',
    'guardian',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'core',
    'product',
    'jazzmin',
    'imagekit',
    'multimedia',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # Needed to login by username in Django admin, regardless of `allauth`
    'allauth.account.auth_backends.AuthenticationBackend', # `allauth` specific authentication methods, such as login by email
    'guardian.backends.ObjectPermissionBackend', # Soporta permisos a nivel de objeto
]


SOCIALACCOUNT_PROVIDERS = {

   'facebook': {
        'APP': {
            'client_id':'561825706412628',
            'secret': '7c6f97138fabfec33f38ab322a51c489'
        },
        'METHOD': 'oauth2',  # Set to 'js_sdk' to use the Facebook connect SDK
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v17.0',
        'GRAPH_API_URL': 'https://graph.facebook.com/v17.0',
    }

}




SOCIALACCOUNT_FORMS = {
    'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
    'signup': 'allauth.socialaccount.forms.SignupForm',
}



ROOT_URLCONF = 'tienda.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'tienda.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tienda_test',  # Nombre de la base de datos
        'USER': 'tienda',  # Usuario de la base de datos
        'PASSWORD': 'thos',  # Contraseña del usuario
        'HOST': 'localhost',  # Servidor donde está la base de datos
        'PORT': '5432',  # Puerto de PostgreSQL (puerto por defecto)
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Lista de idiomas soportados
LANGUAGES = [
    ('es', 'Español'),
    ('en', 'Inglés'),
    ('fr', 'Francés'),  # Agrega más idiomas según lo necesites
]
# Configuración de Parler para manejar las traducciones
PARLER_LANGUAGES = {
    1: (
        {'code': 'es'},  # Idioma predeterminado
        {'code': 'en'},  # Otros idiomas
        {'code': 'fr'},
    ),
    'default': {
        'fallbacks': ['es'],  # Idioma de reserva cuando una traducción no está disponible
        'hide_untranslated': False,  # Muestra aunque no haya traducción
    }
}


LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# settings.py

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Define el directorio donde se recogerán los archivos estáticos en producción
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')

# Directorios adicionales donde Django buscará archivos estáticos
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # Permite login con username o email
ACCOUNT_EMAIL_REQUIRED = True  # El email es requerido
ACCOUNT_EMAIL_VERIFICATION = 'none'  # El email debe ser verificado para activar la cuenta
LOGIN_REDIRECT_URL = '/'  # Redirigir después del login
LOGOUT_REDIRECT_URL = '/' # Redirigir después del logout
SIGNUP_REDIRECT_URL = '/' # Redirigir después del signup
#facebook
AUTH_USER_MODEL = 'auth.User'
ACCOUNT_SIGNUP_FORM_CLASS = 'accounts.forms.CustomSignupForm'

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# Configuración opcional para django-money
DJANGO_MONEY_RATES = {
    'BASE': 'EUR',  # Establece la moneda base, en este caso Euro
    'RATES': {
        'USD': 1.10,  # Tasas de cambio ficticias, estas deben ser dinámicas en producción
        'GBP': 0.85,  # Estos valores son solo ejemplos, en producción usar API de tasas de cambio
    }
}
# Un diccionario para mapear idiomas a monedas
IDIOMA_A_MONEDA = {
    'es': 'EUR',  # Español -> Euro
    'en-gb': 'GBP',  # Inglés del Reino Unido -> Libra
    'en-us': 'USD',  # Inglés de Estados Unidos -> Dólar
    'en': 'USD',
    'fr': 'EUR',  # Francés -> Euro
    # Añade más idiomas según tus necesidades
}


# Listado de monedas permitidas en tu aplicación
CURRENCIES = ('EUR', 'USD', 'GBP')

# Moneda predeterminada
CURRENCY_DEFAULT = 'EUR'

# Configuración opcional para el ckeditor 5
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
CKEDITOR_UPLOAD_PATH = "uploads/"

# Configuración de CKEditor
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['undo', 'redo', '|', 'heading', '|', 'bold', 'italic', 'strikethrough', 'underline', 'link', 'bulletedList', 'numberedList', '|', 'outdent', 'indent', '|', 'blockQuote', 'insertTable', 'mediaEmbed', 'imageUpload', '|', 'removeFormat', 'sourceEditing'],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:inline', 'imageStyle:block', 'imageStyle:side']
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells']
        },
        'simpleUpload': {
            'uploadUrl': 'URL_TO_YOUR_UPLOAD_ENDPOINT',  # Asegúrate de configurar un endpoint para la carga de imágenes
            'headers': {
                'X-CSRFToken': 'CSRF_TOKEN'  # Usar el token CSRF correcto aquí
            }
        },
        'height': '400px',
        'width': 'auto',
    },
    'extends': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', '|', 'blockQuote', 'CKFinder', 'imageUpload', 'undo', 'redo'],
        'image': {
            'toolbar': ['imageStyle:full', 'imageStyle:side', '|', 'imageTextAlternative']
        },
        'ckfinder': {
            'uploadUrl': '/ckfinder_connector/',  # Asegúrate de configurar correctamente la URL de subida
        },
        'height': '400px',
        'width': 'auto',
        'extraPlugins': ','.join([
            'uploadimage',  # Permite la subida de imágenes
            'divarea',      # Mejora la edición de la estructura del documento
            'ckeditor_wiris'  # Plugin para fórmulas matemáticas, si es necesario
        ]),
    }
}

# Jazzmin config

JAZZMIN_SETTINGS = {
    "site_title": "Admin de Mi tienda",
    "site_header": "Mi Tienda",
    "site_brand": "Mi Tienda",
    "welcome_sign": "Bienvenido al Panel de Administración",
    "search_model": "auth.User",
    "user_avatar": None,  # Personaliza esto según tus necesidades
}