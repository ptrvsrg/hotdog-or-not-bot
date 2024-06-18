from aiogram import Router, F
from aiogram.types import CallbackQuery
from i18next import trans as t

from app.bot.callback_data import (
    SubscriptionBuyCallbackFactory,
    MainMenuCallbackFactory,
    SubscriptionCallbackFactory,
)
from app.bot.keyboards import create_subscription_menu, create_subscription_store_menu
from app.service import subscription_service

router = Router(name="subscription")


@router.callback_query(
    MainMenuCallbackFactory.filter(F.action == "show_subscription_store")
)
async def show_subscription_store(callback: CallbackQuery):
    await callback.message.answer(
        t("message.available_subscriptions"),
        reply_markup=create_subscription_store_menu(),
    )


@router.callback_query(SubscriptionCallbackFactory.filter())
async def show_subscription(
    callback: CallbackQuery, callback_data: SubscriptionCallbackFactory
):
    # Find subscription
    subscription = subscription_service.get_by_name(callback_data.name)
    if subscription is None:
        await callback.message.answer(t("error.subscription_not_found"))
        return

    # Get subscription limit
    if subscription.total_daily_predictions == -1:
        limit = t("message.unlimited")
    else:
        limit = subscription.total_daily_predictions

    # Show message
    content = t(
        "message.subscription_profile",
        params={
            "name": subscription.name,
            "limit": limit,
        },
    )
    await callback.message.answer(
        content, reply_markup=create_subscription_menu(subscription.name)
    )


@router.callback_query(SubscriptionBuyCallbackFactory.filter())
async def buy_subscription(callback: CallbackQuery):
    await callback.message.answer(t("message.unsupported_command"))
