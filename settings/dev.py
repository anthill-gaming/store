from .base import *

DEBUG = True
EMAIL_BACKEND = 'anthill.framework.core.mail.backends.console.EmailBackend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'anthill.framework.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'anthill.framework.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'anthill.server': {
            '()': 'anthill.framework.utils.log.ServerFormatter',
            'fmt': '%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'color': True,
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'anthill.server',
        },
        'anthill.server': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'anthill.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'anthill.framework.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'anthill': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'anthill.application': {
            'handlers': ['anthill.server'],
            'level': 'DEBUG',
            'propagate': False
        },
        'tornado.access': {
            'handlers': ['anthill.server'],
            'level': 'DEBUG',
            'propagate': False
        },
        'tornado.application': {
            'handlers': ['anthill.server'],
            'level': 'DEBUG',
            'propagate': False
        },
        'tornado.general': {
            'handlers': ['anthill.server'],
            'level': 'DEBUG',
            'propagate': False
        },
        'celery': {
            'handlers': ['anthill.server'],
            'level': 'DEBUG',
            'propagate': False
        },
        'celery.worker': {
            'handlers': ['anthill.server'],
            'level': 'DEBUG',
            'propagate': False
        },
        'celery.task': {
            'handlers': ['anthill.server'],
            'level': 'DEBUG',
            'propagate': False
        },
        'celery.redirected': {
            'handlers': ['anthill.server'],
            'level': 'DEBUG',
            'propagate': False
        },
        'asyncio': {
            'handlers': ['anthill.server'],
            'level': 'INFO',
            'propagate': False
        },
    }
}

PAYMENT_SYSTEM_BACKENDS = [
    {
        'NAME': 'store.payment.backends.appstore.AppstoreBackend',
        'OPTIONS': {
            'sandbox': True,
        }
    },
    {
        'NAME': 'store.payment.backends.discord.DiscordBackend',
        'OPTIONS': {
            'sandbox': True,
            'client_id': None,
            'client_secret': None
        }
    },
    {
        'NAME': 'store.payment.backends.mailru.MailruBackend',
        'OPTIONS': {
            'sandbox': True,
        }
    },
    {
        'NAME': 'store.payment.backends.steam.SteamBackend',
        'OPTIONS': {
            'sandbox': True,
            'game_id': None,
            'app_ticket_key': None
        }
    },
    {
        'NAME': 'store.payment.backends.xsolla.XsollaBackend',
        'OPTIONS': {
            'sandbox': True,
            'project_id': None,
            'project_key': None,
            'merchant_id': None,
            'api_key': None
        }
    },
]
