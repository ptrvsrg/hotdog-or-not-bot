from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.bot.callback_data import CancelCallbackFactory

router = Router(name="cancel")


@router.callback_query(CancelCallbackFactory.filter())
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
