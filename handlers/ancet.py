

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from loguru import logger

from utils.states import Form, ReportMessage
from data_pack.shedule import get_json
from data_pack.database_ import ancet_me_database, new_clsroom_database
from data_pack.commands_ import send_message_admin


router = Router()

@router.message(Command(commands=['profile', 'me']))
async def me_profile(message: Message, state: FSMContext) -> None:
     answer = await ancet_me_database(message.from_user.id)
          
     if not answer:
          await state.set_state(Form.classroom)
          await message.answer('Напишите свой класс. Пример: 10Б')
               
     else:                    
          await message.answer(answer, parse_mode=ParseMode.HTML)
                      
@router.message(Form.classroom)
async def form_classroom(message: Message, state: FSMContext) -> None:
     await state.update_data(classroom=message.text)
     data_json = await get_json()
     
     if message.text.upper() in data_json.keys():
          await new_clsroom_database(message.text.upper(), message.from_user.id)
          
          await message.answer(f'Данные занесены успешно! Ваш класс {message.text}')
          await state.clear()
          
     else:
          await message.answer('Такого класса не существует! Пример: 10Б')
          
            
@router.message(Command(commands=['report', 'call', 'rp']))
async def call_admin(message: Message, state: FSMContext) -> None:
     await state.set_state(ReportMessage.report)
     await message.answer('Напиши рекомендации для улучшения бота или про найденный баг.')
     
@router.message(ReportMessage.report)
async def reporter(message: Message, state: FSMContext) -> None:
     await state.update_data(report=message.text)
     
     await send_message_admin(message.text, 2054556183, message.from_user.full_name, message.from_user.id)
     logger.info(f'{message.from_user.full_name} send message for admin. ID: {message.from_user.id}')
     
     await message.answer('Сообщение успешно отправлено!')
     await state.clear()
     
     
     
          
     
     
     
     

