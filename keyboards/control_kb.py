from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_button = KeyboardButton(text="Старт")
stop_button = KeyboardButton(text="Стоп")

control_kb = ReplyKeyboardMarkup(
    keyboard=[[start_button, stop_button]],
    resize_keyboard=True
)
