from app.bot.handlers.admin_callbacks_handler import router as admin_router
from app.bot.handlers.cancel_callback_handler import router as cancel_router
from app.bot.handlers.menu_command_handler import router as menu_router
from app.bot.handlers.owner_callbacks_handler import router as owner_router
from app.bot.handlers.predict_images_handler import router as predict_router
from app.bot.handlers.profile_callback_handler import router as profile_router
from app.bot.handlers.start_command_handler import router as start_router
from app.bot.handlers.subscription_callbacks_handler import (
    router as subscription_router,
)

__all__ = [
    "start_router",
    "menu_router",
    "admin_router",
    "owner_router",
    "profile_router",
    "subscription_router",
    "cancel_router",
    "predict_router",
]
