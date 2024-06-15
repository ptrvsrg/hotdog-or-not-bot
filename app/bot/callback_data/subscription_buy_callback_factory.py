from aiogram.filters.callback_data import CallbackData


class SubscriptionBuyCallbackFactory(CallbackData, prefix="subscription_buy"):
    name: str
