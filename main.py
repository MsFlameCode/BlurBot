# Указываем путь к JSON
from asyncio import sleep, exceptions

import aiogram

import datetime
from aiogram.utils.exceptions import BotBlocked
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
import emoji
import const
import keyboard
import statInfo
import process

try:
    bot = Bot(token='...')
    dp = Dispatcher(bot)

    # получим текущую дату:
    date = datetime.datetime.now()
    day = date.day

    if const.LAST_DAY == 0:
        const.LAST_DAY = day


    # сформируем сообщение для отправки

    @dp.message_handler(commands=['start'])
    async def process_start_command(message: types.Message):
        const.user_set.add(message.from_user.id)
        statInfo.check_date(day, message.from_user.id)
        msg = "Привет 😃 \n" \
        "Этот бот  поможет тебе размыть фото или emoji 😎 \n"\
        "А также выгрузить любимые стикеры 😎 \n"\
        "Отправь мне фото, emoji или стикер.\n"
        if message.from_user.id == const.ID_ADMIN:
            await bot.send_message(message.from_user.id, msg, reply_markup=keyboard.create_keyboard_common())
        else:
            await bot.send_message(message.from_user.id, msg)


    @dp.message_handler(content_types=["photo"])
    async def download_photo(message: types.Message):
        const.user_set.add(message.from_user.id)
        statInfo.check_date(day, message.from_user.id)
        const.IS_PHOTO = True
        const.PHOTO_NAME = f"{message.photo[-1].file_id}.jpg"
        # Убедитесь, что каталог /tmp/somedir существует!
        await message.photo[-1].download(destination_file=const.PHOTO_NAME)
        process.blur_image()
        photo = open(const.CUR_NAME, 'rb')
        await bot.send_document(message.chat.id, photo)
        os.remove(const.CUR_NAME, dir_fd=None)
        os.remove(const.PHOTO_NAME, dir_fd=None)
        const.IS_PHOTO = False


    # @dp.message(content_types=types.ContentType.STICKER)
    @dp.message_handler(content_types=["sticker"])
    async def download_sticker(message: types.Message):
        const.user_set.add(message.from_user.id)
        statInfo.check_date(day, message.from_user.id)
        const.STICKER_NAME = f"{message.sticker.file_id}.png"
        await message.sticker.download(destination_file=const.STICKER_NAME)
        sticker = open(const.STICKER_NAME, 'rb')
        await bot.send_document(message.chat.id, sticker)
        # await bot.send_animation(message.chat.id, sticker)
        # await bot.send_animation(message.chat.id, sticker)
        os.remove(const.STICKER_NAME, dir_fd=None)
        if len(const.CUR_NAME):
            os.remove(const.CUR_NAME, dir_fd=None)
        if len(const.PHOTO_NAME):
            os.remove(const.PHOTO_NAME, dir_fd=None)


    @dp.errors_handler(exception=aiogram.utils.exceptions.BotBlocked)
    async def function_name(update: types.Update, exception: aiogram.utils.exceptions.BotBlocked):
        const.BLOCK_COUNT = const.BLOCK_COUNT + 1
        return True


    # обработка кнопки Статистика
    @dp.message_handler(lambda message: message.text == "Статистика")
    async def without_puree(message: types.Message):
        statInfo.check_date(day, message.from_user.id)
        const.user_set.add(message.from_user.id)
        msg = statInfo.create_stat_info()
        await bot.send_message(message.from_user.id, msg, disable_web_page_preview=True)


    @dp.message_handler(content_types=['text'])
    async def handle_text(message):
        const.user_set.add(message.from_user.id)
        statInfo.check_date(day, message.from_user.id)
        # получен emoji если первый символ :
        str_emoji = emoji.demojize(message.text)
        if str_emoji[0] == ':' and len(str_emoji) > 1:
            process.create_blur_emoji(str_emoji)
            if len(const.CUR_NAME) > 0:
                photo = open(const.CUR_NAME, 'rb')
                await bot.send_document(message.chat.id, photo)
                os.remove(const.CUR_NAME, dir_fd=None)

except:
    @dp.message_handler()
    async def echo_message(message: types.Message):
        msg = "В боте возникла ошибка. Попробуйте заново ❤"
        await bot.send_message(message.from_user.id, msg)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
