from aiogram.filters.callback_data import CallbackData


class SelectImageCallbackFactory(CallbackData, prefix="select_image"):
    photo_index: int
    message_id: int
