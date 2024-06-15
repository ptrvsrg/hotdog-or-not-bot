from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from i18next import trans

from app.bot.callback_data import SubscriptionBuyCallbackFactory, CancelCallbackFactory
from app.service import subscription_service


def create_subscription_menu(subscription_name: str) -> InlineKeyboardMarkup:
    subscription = subscription_service.get_by_name(name=subscription_name)

    builder = InlineKeyboardBuilder()
    builder.button(text=trans("button.cancel"),
                   callback_data=CancelCallbackFactory())
    builder.button(text=trans("button.buy_subscription"),
                   callback_data=SubscriptionBuyCallbackFactory(name=subscription.name))
    return builder.as_markup()
