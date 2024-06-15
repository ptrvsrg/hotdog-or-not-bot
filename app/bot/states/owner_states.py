from aiogram.fsm.state import StatesGroup, State


class OwnerStates(StatesGroup):
    awaiting_added_admin = State()
    awaiting_removed_admin = State()
