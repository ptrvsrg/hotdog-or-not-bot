from aiogram.filters.callback_data import CallbackData


class ResultFeedbackCallbackFactory(CallbackData, prefix="result"):
    action: str
    message_id: int
