from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from i18next import trans as t

from app.bot.callback_data import MainMenuCallbackFactory, MainMenuCallbackAction
from app.bot.keyboards import create_cancel_menu
from app.bot.states import OwnerStates
from app.service import user_service, UserNotAdminException, UserAlreadyAdminException

router = Router(name="owner")


@router.callback_query(
    MainMenuCallbackFactory.filter(F.action == MainMenuCallbackAction.ADD_ADMIN)
)
async def add_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        t("message.enter_username"), reply_markup=create_cancel_menu()
    )
    await state.set_state(OwnerStates.awaiting_added_admin)


@router.message(OwnerStates.awaiting_added_admin)
async def process_add(message: Message, state: FSMContext):
    username = message.text
    if username.startswith("@"):
        try:
            user_service.add_admin(username[1:])
            await message.answer(
                t("message.added_admin", params={"username": username})
            )
        except UserAlreadyAdminException as e:
            await message.answer(
                t("error.user_already_admin", params={"username": username})
            )
    else:
        await message.answer(t("error.incorrect_username"))
    await state.clear()


@router.callback_query(
    MainMenuCallbackFactory.filter(F.action == MainMenuCallbackAction.REMOVE_ADMIN)
)
async def remove_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        t("message.enter_username"), reply_markup=create_cancel_menu()
    )
    await state.set_state(OwnerStates.awaiting_removed_admin)


@router.message(OwnerStates.awaiting_removed_admin)
async def process_remove(message: Message, state: FSMContext):
    username = message.text
    if username.startswith("@"):
        try:
            user_service.remove_admin(username[1:])
            await message.answer(
                t("message.removed_admin", params={"username": username})
            )
        except UserNotAdminException as e:
            await message.answer(
                t("error.user_not_admin", params={"username": username})
            )
    else:
        await message.answer(t("error.incorrect_username"))
    await state.clear()
