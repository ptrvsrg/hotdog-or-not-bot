from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from i18next import trans as t

from app.bot.callback_data import (
    ResultFeedbackCallbackFactory,
)


def create_result_feedback_menu(
    message_id: int, is_hotdog: bool
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    success_button = InlineKeyboardButton(
        text=t("button.success"),
        callback_data=ResultFeedbackCallbackFactory(
            is_hotdog=is_hotdog,
            is_success=True,
            message_id=message_id,
        ).pack(),
    )
    fail_button = InlineKeyboardButton(
        text=t("button.fail"),
        callback_data=ResultFeedbackCallbackFactory(
            is_hotdog=is_hotdog,
            is_success=False,
            message_id=message_id,
        ).pack(),
    )

    builder.row(success_button, fail_button)
    return builder.as_markup()
