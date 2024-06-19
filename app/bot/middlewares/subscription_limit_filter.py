from aiogram.filters import BaseFilter
from aiogram.types import Message
from i18next import trans as t

from app.bot.utils.message_utils import (
    get_username_from_message,
)
from app.service import user_service


class SubscriptionLimitFilter(BaseFilter):

    def __init__(self):
        super().__init__()

    async def __call__(self, message: Message) -> bool:
        username = get_username_from_message(message)
        user = user_service.get_user_by_username(username)

        limit_reached = (
            user.subscription.total_daily_predictions != -1
            and user.daily_predictions >= user.subscription.total_daily_predictions
        )

        if limit_reached:
            await message.answer(t("error.subscription_limit"))

        return not limit_reached
