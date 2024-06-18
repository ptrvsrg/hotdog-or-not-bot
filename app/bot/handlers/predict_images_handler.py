import logging

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from i18next import trans

from app.bot.callback_data import SelectImageCallbackFactory, ResultFeedbackCallbackFactory
from app.bot.keyboards import create_select_image_menu, create_result_feedback_menu
from app.bot.middlewares import SubscriptionLimitFilter
from app.bot.utils.callback_utils import get_username_from_callback
from app.bot.utils.file_utils import download_file, create_media_group, \
    extract_photo_map_from_media_group_messages
from app.bot.utils.message_utils import get_photo_from_message, get_username_from_message
from app.bot.utils.state_utils import add_to_state, get_from_state
from app.service import detect_service, predict_service, statistics_service, yandex_disk_service

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

        await answer.delete()
        media_group = create_media_group(cropped_images)
        media_group_messages = await message.answer_media_group(media_group)

        photo_map = extract_photo_map_from_media_group_messages(media_group_messages)
        message_ids = list(photo_map.keys())

        await add_to_state(state, "photo_map", photo_map)
        await media_group_messages[-1].reply(trans("message.select_image"),
                                             reply_markup=create_select_image_menu(message_ids))
        logger.info(f"{username}: Show select image menu")
        return

    # Add to state
    await add_to_state(state, "photo_map", {message.message_id: photo.file_id})

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
                         reply_markup=create_result_feedback_menu(message.message_id, prob >= 0.9))
    logger.info(f"{username}: Hotdog probability {prob}%")


@router.callback_query(SubscriptionLimitFilter(), SelectImageCallbackFactory.filter())
async def process_select_image(callback: CallbackQuery,
                               callback_data: SelectImageCallbackFactory,
                               state: FSMContext):
    username = get_username_from_callback(callback)
    logger.info(f"{username}: Select image with message id {callback_data.message_id}")
    await callback.answer()
    answer = await callback.message.answer(trans("message.image_processing"))

    # Download image
    file_id = (await get_from_state(state, "photo_map"))[str(callback_data.message_id)]
    try:
        logger.info(f"{username}: Downloading image")
        file_bytes = (await download_file(callback.bot, file_id)).read()
    except TelegramBadRequest as e:
        logging.error(e)
        await answer.delete()
        await callback.message.answer(trans("error.file_not_processed"))
        return

    # Predict hotdog
    prob = predict_service.predict(file_bytes)
    prob = round(prob * 100, 4)

    # Add statistics
    if prob >= 0.9:
        statistics_service.add_hotdog_prediction(username)
    else:
        statistics_service.add_not_hotdog_prediction(username)

    # Show result
    await answer.delete()
    await callback.message.answer(trans("message.probability_with_index",
                                        params={"probability": prob, "index": callback_data.index}),
                                  reply_markup=create_result_feedback_menu(callback_data.message_id, prob >= 0.9))
    logger.info(f"{username}: Hotdog probability {prob}%")


@router.callback_query(ResultFeedbackCallbackFactory.filter())
async def feedback_prediction(callback: CallbackQuery,
                              callback_data: ResultFeedbackCallbackFactory,
                              state: FSMContext):
    username = get_username_from_callback(callback)

    # Download image
    file_id = (await get_from_state(state, "photo_map"))[str(callback_data.message_id)]
    try:
        logger.info(f"{username}: Downloading image")
        file_bytes = (await download_file(callback.bot, file_id)).read()
    except TelegramBadRequest as e:
        logging.error(e)
        await callback.message.answer(trans("error.file_not_processed"))
        return

    if callback_data.action.startswith("success"):
        logger.info(f"{username}: Choose successful result")
        statistics_service.add_successful_prediction(username)
    elif callback_data.action.startswith("fail"):
        logger.info(f"{username}: Choose failed result")
        statistics_service.add_failed_predictions(username)

    if callback_data.action in ["success_hotdog", "fail_not_hotdog"]:
        await yandex_disk_service.upload_file(file_bytes, "hotdog")
    if callback_data.action in ["success_not_hotdog", "fail_hotdog"]:
        await yandex_disk_service.upload_file(file_bytes, "not_hotdog")

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(trans("message.thanks_for_feedback"))
