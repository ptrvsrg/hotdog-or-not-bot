from aiogram.types import CallbackQuery


def get_username_from_callback(callback_query: CallbackQuery) -> str:
    return callback_query.from_user.username


def get_user_id_from_callback(callback_query: CallbackQuery) -> int:
    return callback_query.from_user.id
