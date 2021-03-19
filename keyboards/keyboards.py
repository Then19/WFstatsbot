from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Помощь"),
            KeyboardButton("Розыгрыш")
        ]
    ],
    resize_keyboard=True
)