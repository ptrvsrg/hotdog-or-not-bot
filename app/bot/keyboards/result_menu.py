from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from i18next import trans as t

from app.bot.callback_data import ResultFeedbackCallbackFactory


def create_result_feedback_menu(
    message_id: int, is_hotdog: bool
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    suffix = "_hotdog" if is_hotdog else "_not_hotdog"

    success_button = InlineKeyboardButton(
        text=t("button.success"),
        callback_data=ResultFeedbackCallbackFactory(
            action="success" + suffix, message_id=message_id
        ).pack(),
    )
    fail_button = InlineKeyboardButton(
        text=t("button.fail"),
        callback_data=ResultFeedbackCallbackFactory(
            action="fail" + suffix, message_id=message_id
        ).pack(),
    )

    builder.row(success_button, fail_button)
    return builder.as_markup()
