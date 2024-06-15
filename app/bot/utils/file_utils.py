from typing import BinaryIO

from aiogram import Bot


async def download_file(bot: Bot, file_id: str) -> BinaryIO:
    file = await bot.get_file(file_id)
    return await bot.download_file(file.file_path)
