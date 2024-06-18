from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from i18next import trans as t

from app.bot.utils.message_utils import get_username_from_message

router = Router(name="start")


@router.message(Command(commands=["start"]))
async def start(message: Message):
    username = get_username_from_message(message)
    await message.answer(t("message.welcome", params={"user": username}))
