"""
Internal api methods for current service.

Example:

    from anthill.platform.api.internal import as_internal, InternalAPI

    @as_internal()
    async def your_internal_api_method(api: InternalAPI, *params, **options):
        # current_service = api.service
        ...
"""
from anthill.platform.api.internal import as_internal, InternalAPI
from anthill.framework.utils.asynchronous import thread_pool_exec as future_exec
from store.models import Order, Item


@as_internal()
async def create_order(api: InternalAPI,
                       item_id,
                       currency_id,
                       count,
                       payment_backend,
                       user_id,
                       payment_kwargs: dict,
                       store_id=None,
                       **options):
    if store_id is None:
        item = await future_exec(Item.query.get, item_id)
        store_id = item.store.id
    kwargs = {
        'store_id': store_id,
        'item_id': item_id,
        'currency_id': currency_id,
        'user_id': user_id,
        'count': count,
    }
    order = await Order.create_order(payment_backend, payment_kwargs, **kwargs)
    return order.dump()
