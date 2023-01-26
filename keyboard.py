from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import const

def create_keyboard_common():
    button = KeyboardButton('Статистика', callback_data='stat')
    markup = ReplyKeyboardMarkup(resize_keyboard=True).row(button)
    return markup