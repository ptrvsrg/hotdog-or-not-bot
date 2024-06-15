from aiogram.filters.callback_data import CallbackData


class ResultCallbackFactory(CallbackData, prefix="result"):
    action: str
