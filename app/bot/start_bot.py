import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from app.config import config

logger = logging.getLogger("bot")
bot_ = Bot(
    token=config.bot.telegram_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
)
dp = Dispatcher(
    bot=bot_,
    storage=RedisStorage.from_url(
        url="redis://{}:{}@{}:{}/{}".format(
            config.redis.user,
            config.redis.password.get_secret_value(),
            config.redis.host,
            config.redis.port,
            config.redis.db,
        ),
    ),
)


async def start_bot():
    webhook_info = await bot_.get_webhook_info()
    if webhook_info.url != config.bot.webhook_url:
        await bot_.set_webhook(config.bot.webhook_url)
    from app.bot.middlewares import (
        BanMiddleware,
        ExceptionMiddleware,
        CallbackAnswerMiddleware,
        RegisterMiddleware,
    )

    dp.message.outer_middleware(BanMiddleware())
    dp.message.outer_middleware(ExceptionMiddleware())
    dp.message.outer_middleware(RegisterMiddleware())
    dp.callback_query.outer_middleware(BanMiddleware())
    dp.callback_query.outer_middleware(ExceptionMiddleware())
    dp.callback_query.outer_middleware(CallbackAnswerMiddleware())

    from app.bot.handlers import (
        start_router,
        menu_router,
        admin_router,
        owner_router,
        subscription_router,
        profile_router,
        cancel_router,
        predict_router,
    )

    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(admin_router)
    dp.include_router(owner_router)
    dp.include_router(profile_router)
    dp.include_router(subscription_router)
    dp.include_router(cancel_router)
    dp.include_router(predict_router)

    logger.info("Bot started")


async def close_bot():
    await bot_.session.close()
    logger.info("Bot closed")
