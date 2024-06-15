import logging

from aiogram.filters import BaseFilter
from aiogram.types import Message
from i18next import trans

from app.bot.utils.message_utils import get_username_from_message, get_user_id_from_message
from app.service import user_service


class SubscriptionLimitFilter(BaseFilter):

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("SubscriptionLimitMiddleware")

    async def __call__(self, message: Message) -> bool:
        self.logger.debug(f"{message.from_user.id}: Check subscription limit")

        username = get_username_from_message(message)
        user_id = get_user_id_from_message(message)

        user = user_service.get_user_by_username(username)

        result = (user.subscription.total_daily_predictions == -1 or
                  user.daily_predictions < user.subscription.total_daily_predictions)

        if result:
            self.logger.debug(f"{user_id}: Weakly subscription limit not reached")
        else:
            self.logger.debug(f"{user_id}: Weakly subscription limit reached")
            await message.answer(trans("error.subscription_limit"))

        return result
