from aiogram.filters.callback_data import CallbackData


class MainMenuCallbackFactory(CallbackData, prefix="main_menu"):
    action: str
