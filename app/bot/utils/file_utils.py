from typing import BinaryIO

from aiogram import Bot
from aiogram.types import InputMediaPhoto, BufferedInputFile, Message
from aiogram.utils.media_group import MediaGroupBuilder


async def download_file(bot: Bot, file_id: str) -> BinaryIO:
    file = await bot.get_file(file_id)
    return await bot.download_file(file.file_path)


def create_media_group(photos: list[bytes]) -> list[InputMediaPhoto]:
    media_group_builder = MediaGroupBuilder()
    for i, img in enumerate(photos):
        input_file = BufferedInputFile(file=img, filename=f"image_{i}.jpg")
        media_group_builder.add_photo(input_file)
    return media_group_builder.build()


def extract_photo_map_from_media_group_messages(media_group: list[Message]) -> dict:
    photo_map = {}
    for media in media_group:
        photo_map[media.message_id] = media.photo[-1].file_id
    return photo_map
