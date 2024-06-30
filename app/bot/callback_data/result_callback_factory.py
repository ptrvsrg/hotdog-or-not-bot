from aiogram.filters.callback_data import CallbackData


class ResultFeedbackCallbackFactory(CallbackData, prefix="result"):
    is_hotdog: bool
    is_success: bool
    message_id: int
