import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from i18next import trans

from app.bot.callback_data import MainMenuCallbackFactory
from app.bot.keyboards import create_cancel_menu
from app.bot.states import AdminStates
from app.bot.utils.callback_utils import get_username_from_callback
from app.bot.utils.message_utils import get_username_from_message
from app.service import user_service, UserAlreadyBannedException, UserNotBannedException

router = Router(name="admin")
logger = logging.getLogger("admin_callbacks")


@router.callback_query(MainMenuCallbackFactory.filter(F.action == "ban_user"))
async def ban_user(callback: CallbackQuery, state: FSMContext):
    logger.info(f"{get_username_from_callback(callback)}: Start ban user")
    await callback.message.answer(trans("message.enter_username"), reply_markup=create_cancel_menu())
    await state.set_state(AdminStates.awaiting_banned_username)
    logger.info(f"{get_username_from_callback(callback)}: Awaiting username of banned user")


@router.message(AdminStates.awaiting_banned_username)
async def process_ban(message: Message, state: FSMContext):
    logger.info(
        f"{get_username_from_message(message)}: Enter username of banned user {message.text}")
    username = message.text
    if username.startswith('@'):
        try:
            user_service.ban_user(username[1:])
            await message.answer(trans("message.user_is_banned", params={"username": username}))
            logger.info(f"{get_username_from_message(message)}: User {username} is banned")
        except UserAlreadyBannedException as e:
            logger.warning(e)
            await message.answer(trans("error.user_already_banned", params={"username": username}))
    else:
        await message.answer(trans("error.incorrect_username"))
        logger.warning(
            f"{get_username_from_message(message)}: Incorrect username of banned user {username}")
    await state.clear()


@router.callback_query(MainMenuCallbackFactory.filter(F.action == "unban_user"))
async def unban_user(callback: CallbackQuery, state: FSMContext):
    logger.info(f"{get_username_from_callback(callback)}: Start unban user")
    await callback.message.answer(trans("message.enter_username"), reply_markup=create_cancel_menu())
    await state.set_state(AdminStates.awaiting_unbanned_username)
    logger.info(f"{get_username_from_callback(callback)}: Awaiting username of unbanned user")


@router.message(AdminStates.awaiting_unbanned_username)
async def process_ban(message: Message, state: FSMContext):
    username = message.text
    logger.info(f"{get_username_from_message(message)}: Enter username of unbanned user {username}")
    if username.startswith('@'):
        try:
            user_service.unban_user(username[1:])
            await message.answer(trans("message.user_is_unbanned", params={"username": username}))
            logger.info(f"{get_username_from_message(message)}: User {username} is unbanned")
        except UserNotBannedException as e:
            logger.warning(e)
            await message.answer(trans("error.user_not_banned", params={"username": username}))
    else:
        await message.answer(trans("error.incorrect_username"))
        logger.warning(
            f"{get_username_from_message(message)}: Incorrect username of unbanned user {username}")
    await state.clear()


@router.callback_query(MainMenuCallbackFactory.filter(F.action == "list_banned_users"))
async def list_banned_users(callback: CallbackQuery):
    banned_users = user_service.get_banned_users()
    if len(banned_users) > 0:
        content = trans("message.list_banned_users") + "\n"
        for banned_user in banned_users:
            content += "\n@" + banned_user.username
    else:
        content = trans("message.no_banned_users")

    await callback.message.answer(content)
    logger.info(f"{get_username_from_callback(callback)}: List banned users")


@router.callback_query(MainMenuCallbackFactory.filter(F.action == "list_admins"))
async def list_admins(callback: CallbackQuery):
    admins = user_service.get_admins()
    if len(admins) > 0:
        content = trans("message.list_admins") + "\n"
        for admin in admins:
            content += "\n@" + admin.username
    else:
        content = trans("message.no_admins")

    await callback.message.answer(content)
    logger.info(f"{get_username_from_callback(callback)}: List admins")
