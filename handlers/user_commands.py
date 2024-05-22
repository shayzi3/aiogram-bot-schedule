
from aiogram import Router
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from loguru import logger

from Keyboards import reply
from data_pack.shedule import get_json
from data_pack.commands_ import show_today, show_tomorrow, day_of_week
from data_pack.database_ import (
     start_database,
     remove_me_database
)

router = Router()

@router.message(CommandStart())
async def start(message: Message) -> None:
     answer = await start_database(message.from_user.id, message.from_user.full_name)
     
     if answer:
          logger.info(f'New user. Name: {message.from_user.full_name}. ID: {message.from_user.id}')
          
     await message.answer(
          text=f'<b>{message.from_user.first_name.capitalize()}</b>, это бот созданный для комфортного просмотра расписания школы №47 г.Владикавказ. Вся остальная информация после команде /help', 
          reply_markup=reply.board,
          parse_mode=ParseMode.HTML
     )
     
     
          
@router.message(Command(commands=['today', 'Today', 'day', 'Day']))
async def today(message: Message, command: CommandObject) -> None:
     if not command.args:
          return await message.answer('Вы не указали класс. Пример: /today 10Б')
     
     data: dict = await get_json()
     if command.args.upper() not in data.keys():
          return await message.answer('Неверно указан класс! Пример: /today 10Б')
     
     output = await show_today(data, command.args.upper())
     if output == 1:
          return await message.answer('Уроков нет! Можно отдохнуть 😁')
     
     await message.answer(text=output, parse_mode=ParseMode.HTML)
     
     
     
@router.message(Command(commands=['tomorrow', 'next']))
async def tomorrow(message: Message, command: CommandObject) -> None:
     if not command.args:
          return await message.answer('Вы не указали класс. Пример: /next 10Б')
     
     data = await get_json()
     if command.args.upper() not in data.keys():
          return await message.answer('Неверно указан класс! Пример: /next 10Б')
        
     output = await show_tomorrow(data, command.args.upper())
     if output == 1:
          return await message.answer('Завтра нет уроков! Можно отдыхать 😁')
     
     await message.answer(text=output, parse_mode=ParseMode.HTML)
     
     
     
@router.message(Command(commands=['removeme', 'rme']))
async def remove_me(message: Message, command: CommandObject) -> None:
     if not command.args:
          return await message.answer('Вы не указали класс. Пример: /rme 10Б')
     
     data_json = await get_json()
     if command.args.upper() not in data_json.keys():
          return await message.answer('Такого класса не существует! Пример: /rme 10Б')
     
     data_answer = await remove_me_database(command.args.upper(), message.from_user.id)
     if not data_answer:
          return await message.answer('Чтобы поменять класс нужно пройти команду /me')
     
     else:
          await message.answer(f'Вы успешно сменили класс на {command.args}')
          
          
@router.message(Command(commands=['count', 'cn']))
async def day_count(message: Message, command: CommandObject) -> None:
     if not command.args:
          return await message.answer('Не указан номер дня недели. Пример: /count 1')
     
     req = await day_of_week(command.args, message.from_user.id)
     if req is None:
          return await message.answer('Ты сделал что-то не так. Пример: /count [номер дня недели]')
     
     if req is False:
          return await message.answer('Вы не указали свой класс. Используйте команду /me')
     
     if req is True:
          return message.answer('Разве в воскресенье есть уроки??')
     
     await message.answer(req, parse_mode=ParseMode.HTML)
     
     
     
          
          
@router.message(Command(commands=['help', 'hp']))
async def helper(message: Message) -> None:
     value = '''<b>Все команды и как их использовать:</b> 
     \n/today [класс] - узнать уроки сегодня. 
     \n/next [класс] - узнать уроки на завтра.
     \n/me - команда, которая вначале используется чтобы сохранить ваш класс и после чтобы показать ваш профиль.
     \n/rme [класс] - сменить ваш класс.
     \n/call - отправить идею как можно улучшить бота или сообщить о баге.
     \n/count [номер дня недели] - узнать уроки в определённый день.
     \nСегодня 🧾 - после указания класса через команды /me или /rme вам станет доступно расписание класса на сегодня.
     \nЗавтра 📜 - после указания класса через команды /me или /rme вам станет доступно расписание класса на завтра.
     \nЗвонки 🔊 - отобразиться расписание звонков для двух смен.'''
     
     await message.answer(value, parse_mode=ParseMode.HTML)
     
     

     
     