from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from i18next import trans

from app.bot.callback_data import MainMenuCallbackFactory
from app.service import user_service


def create_main_menu(username: str) -> InlineKeyboardMarkup:
    user = user_service.get_user_by_username(username)
    builder = InlineKeyboardBuilder()

    user_buttons = [
        InlineKeyboardButton(text=trans("button.profile"),
                             callback_data=MainMenuCallbackFactory(action="show_profile").pack()),
        InlineKeyboardButton(text=trans("button.subscriptions"),
                             callback_data=MainMenuCallbackFactory(
                                 action="show_subscription_store").pack()),
    ]

    admin_buttons = []
    if user is not None and user.is_admin:
        admin_buttons = [
            InlineKeyboardButton(text=trans("button.ban_user"),
                                 callback_data=MainMenuCallbackFactory(action="ban_user").pack()),
            InlineKeyboardButton(text=trans("button.unban_user"),
                                 callback_data=MainMenuCallbackFactory(action="unban_user").pack()),
            InlineKeyboardButton(text=trans("button.list_banned_users"),
                                 callback_data=MainMenuCallbackFactory(
                                     action="list_banned_users").pack()),
        ]

    owner_buttons = []
    if user is not None and user.is_owner:
        owner_buttons = [
            InlineKeyboardButton(text=trans("button.add_admin"),
                                 callback_data=MainMenuCallbackFactory(action="add_admin").pack()),
            InlineKeyboardButton(text=trans("button.remove_admin"),
                                 callback_data=MainMenuCallbackFactory(
                                     action="remove_admin").pack()),
        ]

    builder.row(*user_buttons, width=2)
    builder.row(*admin_buttons, width=2)
    builder.row(*owner_buttons, width=2)
    return builder.as_markup()