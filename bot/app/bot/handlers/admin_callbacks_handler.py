from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from i18next import trans as t

from bot.app.bot import MainMenuCallbackFactory
from bot.app.bot import create_cancel_menu
from bot.app.bot import AdminStates
from app.service import user_service, UserAlreadyBannedException, UserNotBannedException

router = Router(name="admin")


@router.callback_query(MainMenuCallbackFactory.filter(F.action == "ban_user"))
async def ban_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        t("message.enter_username"), reply_markup=create_cancel_menu()
    )
    await state.set_state(AdminStates.awaiting_banned_username)


@router.message(AdminStates.awaiting_banned_username)
async def process_ban(message: Message, state: FSMContext):
    banned_username = message.text

    if not banned_username.startswith("@"):
        await message.answer(t("error.incorrect_username"))
        await state.clear()
        return

    try:
        user_service.ban_user(banned_username[1:])
        await message.answer(
            t("message.user_is_banned", params={"username": banned_username})
        )
    except UserAlreadyBannedException as e:
        await message.answer(
            t("error.user_already_banned", params={"username": banned_username})
        )
    await state.clear()


@router.callback_query(MainMenuCallbackFactory.filter(F.action == "unban_user"))
async def unban_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        t("message.enter_username"), reply_markup=create_cancel_menu()
    )
    await state.set_state(AdminStates.awaiting_unbanned_username)


@router.message(AdminStates.awaiting_unbanned_username)
async def process_ban(message: Message, state: FSMContext):
    if not username.startswith("@"):
        await message.answer(t("error.incorrect_username"))
        await state.clear()
        return

    try:
        user_service.unban_user(username[1:])
        await message.answer(
            t("message.user_is_unbanned", params={"username": username})
        )
    except UserNotBannedException as e:
        await message.answer(t("error.user_not_banned", params={"username": username}))
    await state.clear()


@router.callback_query(MainMenuCallbackFactory.filter(F.action == "list_banned_users"))
async def list_banned_users(callback: CallbackQuery):
    banned_users = user_service.get_banned_users()
    if len(banned_users) > 0:
        content = t("message.list_banned_users") + "\n"
        for banned_user in banned_users:
            content += "\n@" + banned_user.username
    else:
        content = t("message.no_banned_users")
    await callback.message.answer(content)


@router.callback_query(MainMenuCallbackFactory.filter(F.action == "list_admins"))
async def list_admins(callback: CallbackQuery):
    admins = user_service.get_admins()
    if len(admins) > 0:
        content = t("message.list_admins") + "\n"
        for admin in admins:
            content += "\n@" + admin.username
    else:
        content = t("message.no_admins")
    await callback.message.answer(content)
