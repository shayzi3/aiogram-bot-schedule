
from aiogram import Router
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode

from data_pack.commands_ import calls, send_request
from data_pack.database_ import(
     show_today_database,
     show_tomorrow_database
)

router = Router()

@router.message()
async def echo(message: Message) -> None:
     msg = message.text.lower()[:-1].strip()
     
     if msg == 'звонки':
          output = await calls()
          return await message.answer(text=output, parse_mode=ParseMode.HTML)
     
     
     elif msg == 'сегодня':
          data = await show_today_database(message.from_user.id)
          
          if data is False:
               return await message.answer('Перед использованием этой команды вам нужно пройти команду /me')
          
          elif data == 1:
               return await message.answer('Уроков нет! Можно и отдохнуть.')
          
          return await message.answer(data, parse_mode=ParseMode.HTML)
     
     
     elif msg == 'завтра':
          data = await show_tomorrow_database(message.from_user.id)
          
          if data is False:
               return await message.answer('Перед использованием этой команды вам нужно пройти команду /me')
          
          elif data == 1:
               return await message.answer('Уроков завтра нет! Можно и отдохнуть.')
          
          return await message.answer(data, parse_mode=ParseMode.HTML)
          
     answer = await send_request()
     if answer:
          await message.answer(text=f'<i>{answer[0]}</i> <b>{answer[1]}</b>', parse_mode=ParseMode.HTML)
          
     
          
     
     
