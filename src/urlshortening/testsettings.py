INITIAL_URL_LEN = 6
RETRY_COUNT = 5
SHORT_URL_PATH = 'http://example.com/short-prefix/'
REDIRECT_PREFIX = 'r'

DEBUG = TEMPLATE_DEBUG = True
SECRET_KEY = '123'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

INSTALLED_APPS = ['urlshortening']
ROOT_URLCONF = ['urlshortening.urls']
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
