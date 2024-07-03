from aiogram import Router, F
from aiogram.types import CallbackQuery
from i18next import trans as t

from app.bot.callback_data import MainMenuCallbackFactory, MainMenuCallbackAction
from app.bot.utils.callback_utils import get_username_from_callback
from app.config import config
from app.service import user_service

router = Router(name="profile")


@router.callback_query(
    MainMenuCallbackFactory.filter(F.action == MainMenuCallbackAction.SHOW_PROFILE)
)
async def show_profile(callback: CallbackQuery):
    # Find user
    username = get_username_from_callback(callback)
    user = user_service.get_user_by_username(username)
    if user is None:
        await callback.message.answer(t("error.user_not_found"))
        return

    # Get role
    if user.is_owner:
        role = t("message.owner")
    elif user.is_admin:
        role = t("message.admin")
    else:
        role = t("message.user")

    # Get limit status
    remaining_predictions = config.bot.daily_limit - user.statistics.daily_predictions
    limit_remainder = f"{remaining_predictions}/{config.bot.daily_limit}"

    # Show message
    content = t(
        "message.user_profile",
        params={
            "username": user.username,
            "role": role,
            "total_predictions": user.statistics.total_predictions,
            "daily_predictions": user.statistics.daily_predictions,
            "hotdog_predictions": user.statistics.hotdog_predictions,
            "not_hotdog_predictions": user.statistics.not_hotdog_predictions,
            "successful_predictions": user.statistics.successful_predictions,
            "failed_predictions": user.statistics.failed_predictions,
            "limit_remainder": limit_remainder,
        },
    )
    await callback.message.answer(content)
