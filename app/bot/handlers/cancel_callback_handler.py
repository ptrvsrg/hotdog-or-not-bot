import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from i18next import trans

from app.bot.callback_data import CancelCallbackFactory
from app.bot.utils.callback_utils import get_username_from_callback

router = Router(name="cancel")
logger = logging.getLogger("cancel")


@router.callback_query(CancelCallbackFactory.filter())
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(trans("message.canceled"))
    await state.clear()
    logger.info(f"{get_username_from_callback(callback)}: Cancel the operation")
