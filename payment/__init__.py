from anthill.framework.utils.module_loading import import_string
from anthill.framework.core.exceptions import ImproperlyConfigured
from anthill.framework.conf import settings


def _get_backends(return_tuples=False):
    backends = []
    for backend_data in settings.PAYMENT_SYSTEM_BACKENDS:
        backend_path = backend_data['NAME']
        backend_options = backend_data.get('OPTIONS', {})
        try:
            backend_class = import_string(backend_path)
        except ImportError:
            msg = "The module in NAME could not be imported: %s." \
                  "Check your PAYMENT_SYSTEM_BACKENDS setting."
            raise ImproperlyConfigured(msg % backend_data['NAME'])
        backend = backend_class(**backend_options)
        backends.append((backend, backend_path) if return_tuples else backend)
    if not backends:
        raise ImproperlyConfigured(
            'No payment system backends have been defined. '
            'Does PAYMENT_SYSTEM_BACKENDS contain anything?'
        )
    return backends


def get_backends():
    return _get_backends(return_tuples=False)
