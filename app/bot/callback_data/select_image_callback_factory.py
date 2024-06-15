from aiogram.filters.callback_data import CallbackData


class SelectImageCallbackFactory(CallbackData, prefix="select_image"):
    index: int
