import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from app.bot.utils.message_utils import get_username_from_message, get_user_id_from_message
from app.service import user_service


class RegisterMiddleware(BaseMiddleware):

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("RegisterMiddleware")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        self.logger.debug(f"{event.from_user.id}: Check user registration")
        username = get_username_from_message(event)
        user = user_service.get_user_by_username(username)
        if user is None:
            user_service.create_user(username)
            self.logger.info(f"{get_user_id_from_message(event)}: Register user {username}")
        return await handler(event, data)