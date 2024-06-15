from aiogram.filters.callback_data import CallbackData


class SubscriptionCallbackFactory(CallbackData, prefix="subscription"):
    name: str
