from anthill.framework.utils.module_loading import import_string
from anthill.framework.core.exceptions import ImproperlyConfigured
from anthill.framework.conf import settings
from .exceptions import PaymentFailed


def _get_backends(return_tuples=False):
    backends = []
    for backend_data in settings.PAYMENT_SYSTEM_BACKENDS:
        path = backend_data['NAME']
        options = backend_data.get('OPTIONS', {})
        try:
            backend_class = import_string(path)
        except ImportError:
            msg = "The module in NAME could not be imported: %s." \
                  "Check your PAYMENT_SYSTEM_BACKENDS setting."
            raise ImproperlyConfigured(msg % path)
        backend = backend_class(**options)
        backends.append((path, backend) if return_tuples else backend)
    if not backends:
        raise ImproperlyConfigured(
            'No payment system backends have been defined. '
            'Does PAYMENT_SYSTEM_BACKENDS contain anything?'
        )
    return backends


def get_backends():
    return _get_backends(return_tuples=False)


def get_backend(path):
    return dict(_get_backends(return_tuples=True))[path]


async def create_order(backend_name, order, **kwargs):
    backend = get_backend(backend_name)
    try:
        result = await backend.create_order(order, **kwargs)
    except Exception as e:
        raise PaymentFailed from e
    return result
