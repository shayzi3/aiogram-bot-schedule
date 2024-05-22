
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from loguru import logger

from data_pack.database_ import show_admin_users
from data_pack.commands_ import send_message_all_users, send_message_one_user
from utils.states import MessageSender, MsgUser

router = Router()

@router.message(Command(commands=['all', 'users']))
async def users(message: Message) -> None:
     admin = '2054556183'
     
     if str(message.from_user.id) == admin:
          users: list = await show_admin_users()
          await message.answer(f'Кол-во пользователей: {users[1]} \n\n{users[0]}')
          
     else:
          await message.answer('Ты не являешься админом бота.')
          
          
          
@router.message(Command(commands=['msg']))
async def msg_user(message: Message, state: FSMContext) -> None:
     admin = '2054556183'
     
     if str(message.from_user.id) == admin:
          await state.set_state(MsgUser.id_)
          await message.answer('Отправь id.')
          
     else:
          await message.answer('Ты не являешься админом бота.')
          
@router.message(MsgUser.id_)
async def id_user(message: Message, state: FSMContext) -> None:
     await state.update_data(id_=message.text)
     await state.set_state(MsgUser.msg_one_user)
     
     await message.answer('Теперь отправь сообщение.')
     
@router.message(MsgUser.msg_one_user)
async def msg_for_user(message: Message, state: FSMContext) -> None:
     await state.update_data(msg_one_user=message.text)
     data = await state.get_data()
     
     await send_message_one_user(data['msg_one_user'], data['id_'])
     logger.info(f'Admin send message for {data["id_"]}')
     
     await message.answer('Сообщение отправлено успешно!')
     await state.clear()
     
     
     
@router.message(Command(commands=['adt', 'advt']))
async def adt_message(messsage: Message, state: FSMContext) -> None:
     admin = '2054556183'
     
     if str(messsage.from_user.id) == admin:
          await state.set_state(MessageSender.message_send)
          await messsage.answer('Напиши объявление.')
          
     else:
          await messsage.answer('Ты не являешься админом бота.')
    
@router.message(MessageSender.message_send)
async def message_sender(message: Message, state: FSMContext) -> None:
     await state.update_data(message_send=message.text)
     
     await send_message_all_users(message.text)
     logger.info('Admin send adt all users.')
     
     await message.answer('Объявление отправлено успешно!')
     await state.clear()
