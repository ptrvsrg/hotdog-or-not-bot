from aiogram.types import Update
from fastapi import FastAPI, Request, Response

from app.bot import bot_, dp
from app.config import config

app = FastAPI(
    name="Hotdog or Not Bot",
    version="{}.{}.{}".format(
        config.application.major_version,
        config.application.minor_version,
        config.application.patch_version,
    ),
    debug=config.server.debug,
)


@app.post("/webhook")
async def webhook(request: Request):
    update = Update(**await request.json())
    await dp.feed_webhook_update(bot_, update)
    return Response(status_code=200)


@app.on_event("startup")
async def on_startup():
    from app.db import connect_db

    connect_db()

    from app.bot import start_bot

    await start_bot()

    from app.scheduler import start_scheduler

    start_scheduler()


@app.on_event("shutdown")
async def on_shutdown():
    from app.scheduler import stop_scheduler

    stop_scheduler()

    from app.bot import close_bot

    await close_bot()

    from app.db import disconnect_db

    disconnect_db()


__all__ = ["app"]
