from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from i18next import trans as t

from app.bot.callback_data import SelectImageCallbackFactory, CancelCallbackFactory


def create_select_image_menu(message_ids: list[int]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    image_buttons = []
    for i, message_id in enumerate(message_ids):
        image_buttons += [
            InlineKeyboardButton(
                text=str(i + 1),
                callback_data=SelectImageCallbackFactory(
                    index=i + 1, message_id=message_id
                ).pack(),
            )
        ]

    cancel_button = InlineKeyboardButton(
        text=t("button.cancel"), callback_data=CancelCallbackFactory().pack()
    )

    builder.row(*image_buttons, width=2)
    builder.row(cancel_button)
    return builder.as_markup()
