from aiogram.fsm.context import FSMContext


async def add_to_state(state: FSMContext, key: str, value):
    state_data = await state.get_data()
    if state_data is None:
        state_data = {}

    if key not in state_data:
        state_data[key] = value
    else:
        state_data[key] = {**value, **state_data[key]}

    await state.set_data(state_data)


async def get_from_state(state: FSMContext, key: str):
    state_data = await state.get_data()
    if state_data is None:
        return {}
    return state_data[key]
