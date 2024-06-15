from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from i18next import trans

from app.bot.callback_data import ResultCallbackFactory


def create_result_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    success_button = InlineKeyboardButton(text=trans("button.success"),
                                          callback_data=ResultCallbackFactory(
                                              action="success").pack())
    fail_button = InlineKeyboardButton(text=trans("button.fail"),
                                       callback_data=ResultCallbackFactory(action="fail").pack())

    builder.row(success_button, fail_button)
    return builder.as_markup()
