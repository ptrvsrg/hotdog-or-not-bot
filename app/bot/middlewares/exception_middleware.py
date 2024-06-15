import logging
from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message
from i18next import trans


class ExceptionMiddleware(BaseMiddleware):

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            self.logger.exception(e)
            if isinstance(event, CallbackQuery):
                await event.message.answer(trans("error.internal"))
            else:
                await event.answer(trans("error.internal"))
