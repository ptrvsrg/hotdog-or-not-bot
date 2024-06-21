from typing import Any

from aiogram.filters.callback_data import CallbackData


class CancelCallbackFactory(CallbackData, prefix="cancel"):

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
