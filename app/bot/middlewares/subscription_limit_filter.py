from aiogram.filters import BaseFilter
from aiogram.types import Message
from i18next import trans as t

from app.bot.utils.message_utils import (
    get_username_from_message,
)
from app.service import user_service
from app.config import config


class SubscriptionLimitFilter(BaseFilter):

    def __init__(self):
        super().__init__()

    async def __call__(self, message: Message) -> bool:
        username = get_username_from_message(message)
        user = user_service.get_user_by_username(username)

        limit_reached = user.daily_predictions >= config.bot.daily_limit

        if limit_reached:
            await message.answer(t("error.subscription_limit"))

        return not limit_reached
