import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from i18next import trans

from app.bot.callback_data import MainMenuCallbackFactory
from app.bot.keyboards import create_cancel_menu
from app.bot.states import OwnerStates
from app.bot.utils.callback_utils import get_username_from_callback
from app.bot.utils.message_utils import get_username_from_message
from app.service import user_service, UserNotAdminException, UserAlreadyAdminException

router = Router(name="owner")
logger = logging.getLogger("owner")


@router.callback_query(MainMenuCallbackFactory.filter(F.action == "add_admin"))
async def add_admin(callback: CallbackQuery, state: FSMContext):
    logger.info(f"{get_username_from_callback(callback)}: Start adding admin")
    await callback.message.answer(trans("message.enter_username"), reply_markup=create_cancel_menu())
    await state.set_state(OwnerStates.awaiting_added_admin)
    logger.info(f"{get_username_from_callback(callback)}: Awaiting admin username")


@router.message(OwnerStates.awaiting_added_admin)
async def process_add(message: Message, state: FSMContext):
    logger.info(f"{get_username_from_message(message)}: Entered admin username {message.text}")
    username = message.text
    if username.startswith('@'):
        try:
            user_service.add_admin(username[1:])
            await message.answer(trans("message.added_admin", params={"username": username}))
            logger.info(f"{get_username_from_message(message)}: Added admin {username}")
        except UserAlreadyAdminException as e:
            logger.warning(e)
            await message.answer(trans("error.user_already_admin", params={"username": username}))
    else:
        await message.answer(trans("error.incorrect_username"))
        logger.info(f"{get_username_from_message(message)}: Incorrect username {username}")
    await state.clear()


@router.callback_query(MainMenuCallbackFactory.filter(F.action == "remove_admin"))
async def remove_admin(callback: CallbackQuery, state: FSMContext):
    logger.info(f"{get_username_from_callback(callback)}: Start removing admin")
    await callback.message.answer(trans("message.enter_username"), reply_markup=create_cancel_menu())
    await state.set_state(OwnerStates.awaiting_removed_admin)
    logger.info(f"{get_username_from_callback(callback)}: Awaiting admin username")


@router.message(OwnerStates.awaiting_removed_admin)
async def process_remove(message: Message, state: FSMContext):
    logger.info(f"{get_username_from_message(message)}: Entered admin username {message.text}")
    username = message.text
    if username.startswith('@'):
        try:
            user_service.remove_admin(username[1:])
            await message.answer(trans("message.removed_admin", params={"username": username}))
            logger.info(f"{get_username_from_message(message)}: Removed admin {username}")
        except UserNotAdminException as e:
            logger.warning(e)
            await message.answer(trans("error.user_not_admin", params={"username": username}))
    else:
        await message.answer(trans("error.incorrect_username"))
        logger.info(f"{get_username_from_message(message)}: Incorrect username {username}")
    await state.clear()
