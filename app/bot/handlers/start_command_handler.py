import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from i18next import trans

from app.bot.utils.message_utils import get_username_from_message

router = Router(name="start")
logger = logging.getLogger("start")


@router.message(Command(commands=["start"]))
async def start(message: Message):
    username = get_username_from_message(message)
    await message.answer(trans("message.welcome", params={"user": username}))
    logger.info(f"{get_username_from_message(message)}: Started bot")
