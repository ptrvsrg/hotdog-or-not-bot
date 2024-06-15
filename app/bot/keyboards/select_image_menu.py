from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from i18next import trans

from app.bot.callback_data import SelectImageCallbackFactory, CancelCallbackFactory


def create_select_image_menu(image_count: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    image_buttons = []
    for i in range(image_count):
        image_buttons += [
            InlineKeyboardButton(text=str(i + 1),
                                 callback_data=SelectImageCallbackFactory(index=i).pack())
        ]

    cancel_button = InlineKeyboardButton(text=trans("button.cancel"),
                                         callback_data=CancelCallbackFactory().pack())

    builder.row(*image_buttons, width=2)
    builder.row(cancel_button)
    return builder.as_markup()
