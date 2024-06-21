from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from i18next import trans as t

from bot.app.bot import CancelCallbackFactory


def create_cancel_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    cancel_button = InlineKeyboardButton(
        text=t("button.cancel"), callback_data=CancelCallbackFactory().pack()
    )
    builder.row(cancel_button)
    return builder.as_markup()
