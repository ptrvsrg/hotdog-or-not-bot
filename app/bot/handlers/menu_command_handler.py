from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from i18next import trans as t

from app.bot.keyboards import create_main_menu
from app.bot.utils.message_utils import get_username_from_message

router = Router(name="menu")


@router.message(Command(commands=["menu"]))
async def menu(message: Message):
    username = get_username_from_message(message)
    await message.answer(
        t("message.available_commands"), reply_markup=create_main_menu(username)
    )
