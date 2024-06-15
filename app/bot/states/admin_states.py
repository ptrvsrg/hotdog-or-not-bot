from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    awaiting_banned_username = State()
    awaiting_unbanned_username = State()
