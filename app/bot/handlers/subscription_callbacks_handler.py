import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery
from i18next import trans

from app.bot.callback_data import SubscriptionBuyCallbackFactory, MainMenuCallbackFactory, \
    SubscriptionCallbackFactory
from app.bot.keyboards import create_subscription_menu, create_subscription_store_menu
from app.bot.utils.callback_utils import get_username_from_callback
from app.service import subscription_service

router = Router(name="subscription")
logger = logging.getLogger("subscription")


@router.callback_query(MainMenuCallbackFactory.filter(F.action == "show_subscription_store"))
async def show_subscription_store(callback: CallbackQuery):
    await callback.message.answer(trans("message.available_subscriptions"),
                                  reply_markup=create_subscription_store_menu())
    logger.info(f"{get_username_from_callback(callback)}: Show subscription store")


@router.callback_query(SubscriptionCallbackFactory.filter())
async def show_subscription(callback: CallbackQuery, callback_data: SubscriptionCallbackFactory):
    subscription = subscription_service.get_by_name(callback_data.name)
    if subscription is None:
        await callback.message.answer(trans("error.subscription_not_found"))
        return

    if subscription.total_daily_predictions == -1:
        limit = trans("message.unlimited")
    else:
        limit = subscription.total_daily_predictions

    content = trans(
        "message.subscription_profile",
        params={
            "name": subscription.name,
            "limit": limit,
        },
    )
    await callback.message.answer(content,
                                  reply_markup=create_subscription_menu(subscription.name))
    logger.info(f"{get_username_from_callback(callback)}: Show subscription {subscription.name}")


@router.callback_query(SubscriptionBuyCallbackFactory.filter())
async def buy_subscription(callback: CallbackQuery):
    await callback.message.answer(trans("message.unsupported_command"))
