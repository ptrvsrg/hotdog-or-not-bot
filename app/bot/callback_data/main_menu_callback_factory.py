from enum import Enum

from aiogram.filters.callback_data import CallbackData


class MainMenuCallbackAction(Enum):
    SHOW_PROFILE = "show_profile"
    BAN_USER = "ban_user"
    UNBAN_USER = "unban_user"
    SHOW_BANNED_USERS = "show_banned_users"
    SHOW_ADMINS = "show_admins"
    ADD_ADMIN = "add_admin"
    REMOVE_ADMIN = "remove_admin"


class MainMenuCallbackFactory(CallbackData, prefix="main_menu"):
    action: MainMenuCallbackAction
