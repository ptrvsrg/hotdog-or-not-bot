import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery


class CallbackAnswerMiddleware(BaseMiddleware):

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("CallbackAnswerMiddleware")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        self.logger.debug(f"{event.from_user.id}: Callback auto answer")
        await event.answer()
        return await handler(event, data)
