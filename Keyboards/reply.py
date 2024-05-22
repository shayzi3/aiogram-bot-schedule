
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


board = ReplyKeyboardMarkup(
     keyboard=[
          [
               KeyboardButton(text='Сегодня 🧾'),
               KeyboardButton(text='Завтра 📜'),
               KeyboardButton(text='Звонки 🔊')
          ]
     ],
     resize_keyboard=True,   # Уменьшение кнопок
     one_time_keyboard=True  # Убирается панель после использования
)