from aiogram.types import Message, PhotoSize


def get_username_from_message(message: Message) -> str:
    return message.from_user.username


def get_user_id_from_message(message: Message) -> str:
    return message.from_user.username


def get_photo_from_message(message: Message) -> PhotoSize:
    return message.photo[-1]
