import logging
from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from i18next import trans

from app.service import user_service


class BanMiddleware(BaseMiddleware):

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("BanMiddleware")

    def is_enabled(self, username: str) -> bool:
        user = user_service.get_user_by_username(username)
        return not user or not user.is_banned

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        self.logger.debug(f"{event.from_user.id}: Check ban status")

        username = event.from_user.username
        if self.is_enabled(username):
            self.logger.debug(f"{event.from_user.id}: User not banned")
            return await handler(event, data)

        self.logger.debug(f"{event.from_user.id}: User banned")
        if isinstance(event, CallbackQuery):
            await event.message.answer(trans("error.user_banned"))
        else:
            await event.answer(trans("error.user_banned"))
