from aiogram.filters import BaseFilter
from aiogram.types import Message
from i18next import trans as t

from app.bot.utils.message_utils import (
    get_username_from_message,
)
from app.service import statistics_service
from app.config import config


class SubscriptionLimitFilter(BaseFilter):

    def __init__(self):
        super().__init__()

    async def __call__(self, message: Message) -> bool:
        username = get_username_from_message(message)
        statistics = statistics_service.get_statistics(username)

        limit_reached = statistics.daily_predictions >= config.bot.daily_limit

        if limit_reached:
            await message.answer(t("error.subscription_limit"))

        return not limit_reached
