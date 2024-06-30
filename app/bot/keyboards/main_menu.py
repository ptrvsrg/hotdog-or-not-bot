from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from i18next import trans as t

from app.bot.callback_data import MainMenuCallbackFactory, MainMenuCallbackAction
from app.service import user_service


def create_main_menu(username: str) -> InlineKeyboardMarkup:
    user = user_service.get_user_by_username(username)
    builder = InlineKeyboardBuilder()

    user_buttons = [
        InlineKeyboardButton(
            text=t("button.profile"),
            callback_data=MainMenuCallbackFactory(
                action=MainMenuCallbackAction.SHOW_PROFILE
            ).pack(),
        ),
    ]

    admin_buttons = []
    if user is not None and user.is_admin:
        admin_buttons = [
            InlineKeyboardButton(
                text=t("button.ban_user"),
                callback_data=MainMenuCallbackFactory(
                    action=MainMenuCallbackAction.BAN_USER
                ).pack(),
            ),
            InlineKeyboardButton(
                text=t("button.unban_user"),
                callback_data=MainMenuCallbackFactory(
                    action=MainMenuCallbackAction.UNBAN_USER
                ).pack(),
            ),
            InlineKeyboardButton(
                text=t("button.list_banned_users"),
                callback_data=MainMenuCallbackFactory(
                    action=MainMenuCallbackAction.SHOW_BANNED_USERS
                ).pack(),
            ),
            InlineKeyboardButton(
                text=t("button.list_admins"),
                callback_data=MainMenuCallbackFactory(
                    action=MainMenuCallbackAction.SHOW_ADMINS
                ).pack(),
            ),
        ]

    owner_buttons = []
    if user is not None and user.is_owner:
        owner_buttons = [
            InlineKeyboardButton(
                text=t("button.add_admin"),
                callback_data=MainMenuCallbackFactory(action="add_admin").pack(),
            ),
            InlineKeyboardButton(
                text=t("button.remove_admin"),
                callback_data=MainMenuCallbackFactory(action="remove_admin").pack(),
            ),
        ]

    builder.row(*user_buttons, width=2)
    builder.row(*admin_buttons, width=2)
    builder.row(*owner_buttons, width=2)
    return builder.as_markup()
