import logging

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile, CallbackQuery
from aiogram.utils.media_group import MediaGroupBuilder
from i18next import trans

from app.bot.callback_data import SelectImageCallbackFactory, ResultCallbackFactory
from app.bot.keyboards import create_select_image_menu, create_result_menu
from app.bot.middlewares import SubscriptionLimitFilter
from app.bot.utils.callback_utils import get_username_from_callback
from app.bot.utils.file_utils import download_file
from app.bot.utils.message_utils import get_photo_from_message, get_username_from_message
from app.service import detect_service, predict_service, statistics_service, user_service
from app.utils.image_utils import postprocess_image

router = Router(name="predict")
logger = logging.getLogger("predict")


@router.message(SubscriptionLimitFilter(), F.photo)
async def predict_images(message: Message, bot: Bot, state: FSMContext):
    username = get_username_from_message(message)
    logger.info(f"{username}: Start prediction")

    # Get one image
    photo = get_photo_from_message(message)
    if photo.file_size > 52428800:
        await message.answer(trans("error.image_too_big"))
        logger.exception(f"{username}: Image too big")
        return

    answer = await message.answer(trans("message.image_processing"))

    # Download image
    try:
        logger.info(f"{username}: Downloading image")
        file_bytes = (await download_file(bot, photo.file_id)).read()
    except TelegramBadRequest as e:
        logging.error(e)
        await answer.delete()
        await message.answer(trans("error.file_not_processed"))
        return

    # Detect all objects in the image
    cropped_images = detect_service.detect_all(file_bytes)

    # Use initial image if no objects are detected
    if len(cropped_images) == 0:
        cropped_images = [file_bytes]

    #  User must select one image if more than one is detected
    if len(cropped_images) > 1:
        logger.info(f"{username}: More than one object detected")
        media_group_builder = MediaGroupBuilder()
        for i, img in enumerate(cropped_images):
            input_file = BufferedInputFile(file=img, filename=f"cropped_image_{i}.jpg")
            media_group_builder.add_photo(input_file)

        await answer.delete()
        media_group_messages = await message.answer_media_group(media_group_builder.build())
        file_ids = [message.photo[-1].file_id for message in media_group_messages]
        await state.set_data(data={"file_ids": file_ids})
        await media_group_messages[-1].reply(trans("message.select_image"),
                                             reply_markup=create_select_image_menu(len(file_ids)))
        logger.info(f"{username}: Show select image menu")
        return

    # Predict hotdog if one image is detected
    prob = predict_service.predict(cropped_images[0])
    prob = round(prob * 100, 4)

    # Add statistics
    if prob >= 0.9:
        statistics_service.add_hotdog_prediction(username)
    else:
        statistics_service.add_not_hotdog_prediction(username)

    # Show result
    await answer.delete()
    await message.answer(trans("message.probability",
                               params={"probability": prob}),
                         reply_markup=create_result_menu())
    logger.info(f"{username}: Hotdog probability {prob}%")


@router.callback_query(SubscriptionLimitFilter(), SelectImageCallbackFactory.filter())
async def process_select_image(callback: CallbackQuery,
                               callback_data: SelectImageCallbackFactory,
                               state: FSMContext):
    username = get_username_from_callback(callback)
    logger.info(f"{username}: Select image {callback_data.index}")
    await callback.answer()

    # Get image
    file_id = (await state.get_data())["file_ids"][callback_data.index]

    answer = await callback.message.answer(trans("message.image_processing"))

    # Download image
    try:
        logger.info(f"{username}: Downloading image")
        file_bytes = await download_file(callback.bot, file_id)
    except TelegramBadRequest as e:
        logging.error(e)
        await answer.delete()
        await callback.message.answer(trans("error.file_not_processed"))
        return

    # Predict hotdog
    prob = predict_service.predict(file_bytes.read())
    prob = round(prob * 100, 4)

    # Add statistics
    if prob >= 0.9:
        statistics_service.add_hotdog_prediction(username)
    else:
        statistics_service.add_not_hotdog_prediction(username)

    # Show result
    await answer.delete()
    await callback.message.answer(trans("message.probability_with_index",
                                        params={"probability": prob,
                                                "index": callback_data.index + 1}),
                                  reply_markup=create_result_menu())
    logger.info(f"{username}: Hotdog probability {prob}%")


@router.callback_query(ResultCallbackFactory.filter())
async def feedback_prediction(callback: CallbackQuery, callback_data: ResultCallbackFactory):
    username = get_username_from_callback(callback)
    if callback_data.action == "success":
        logger.info(f"{username}: Choose successful result")
    else:
        logger.info(f"{username}: Choose failed result")

    # Add statistics
    if callback_data.action == "success":
        statistics_service.add_successful_prediction(username)
    else:
        statistics_service.add_failed_predictions(username)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(trans("message.thanks_for_feedback"))
