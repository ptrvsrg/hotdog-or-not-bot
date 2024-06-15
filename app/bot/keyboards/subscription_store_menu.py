from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from i18next import trans

from app.bot.callback_data import SubscriptionCallbackFactory, CancelCallbackFactory
from app.service import subscription_service


def create_subscription_store_menu() -> InlineKeyboardMarkup:
    subscriptions = subscription_service.get_all()

    builder = InlineKeyboardBuilder()
    subscription_buttons = []
    for subscription in subscriptions:
        subscription_buttons += [
            InlineKeyboardButton(text=subscription.name,
                                 callback_data=SubscriptionCallbackFactory(
                                     name=subscription.name).pack())
        ]

    cancel_button = InlineKeyboardButton(text=trans("button.cancel"),
                                         callback_data=CancelCallbackFactory().pack())

    builder.row(*subscription_buttons, width=2)
    builder.row(cancel_button)
    return builder.as_markup()
