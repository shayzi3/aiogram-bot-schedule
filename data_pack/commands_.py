import asyncio
import os

import aiohttp

from datetime import datetime as dt

from aiogram.utils import markdown
from aiogram import Bot
from loguru import logger

from data_pack.shedule import time_1, time_2, days
from data_pack import database_ as dtb
from data_pack import shedule as sh


async def show_today(data: dict, class_: str) -> str:
     day_ = dt.now().weekday()
     
     if day_ + 1 == len(days) + 1: return 1
     
     check = days[day_]
     
     list_lessons: list = data[class_][check]
     output = f'День: {check}. Класс {class_}'
     new = []
     
     value = time_1 if not list_lessons[0].isspace() else time_2
     for i in list_lessons:
          if not i.isspace():
               new.append(await sorted_text(i))
                                         
     for x in range(len(new)):
          output += f'\n\n{x + 1} урок. Время: {value[x]} \n {new[x]}'
               
     return markdown.hblockquote(output)


async def show_tomorrow(data: dict, class_: str) -> str:
     day_ = dt.now().weekday()
     
     if day_ == len(days) - 1: return 1
     
     check = days[day_ + 1 if day_ + 1 != len(days) + 1 else 0]
     
     list_lessons: list = data[class_][check]
     output = f'День: {check}. Класс: {class_}'
     new = []
     
     value = time_1 if not list_lessons[0].isspace() else time_2
     for i in list_lessons:
          if not i.isspace():
               new.append(await sorted_text(i))
                    
     for x in range(len(new)):
          output += f'\n\n{x + 1} урок. Время: {value[x]} \n {new[x]}'  
          
     return markdown.hblockquote(output)  


async def sorted_text(lesson: str) -> str:
     if len(lesson.split(':')) > 1:
          value = lesson.split(':')[-1][1:]   # ? Кабинеты, которые нужно разбить
          main_ = lesson.split('/')            # ? Разбиваю на два учителя
          
          if len(value) == 3:
               sort_ = main_[0][:-3]
               
               del main_[0]
               main_.append(sort_)
               
               main_[0] = main_[0] + f' {value}'
               
               return ''.join(main_)
          
          elif len(value) == 2:
               sort_ = main_[0][:-2]
               
               del main_[0]
               main_.append(sort_)
               
               main_[0] = main_[0] + f' {value}'
               
               return ''.join(main_)
               
               
          elif len(value) == 4:
               sort = main_[1][:-4]
               s = [value[:-2], value[2:]]
                                   
                    
          elif len(value) == 5:
               sort = main_[1][:-5]
               s = [value[:-3], value[2:]]
                    
          elif len(value) == 6:
               sort = main_[1][:-6]     # ? Получаю значение второго учителя без кабинетов, только с номером группы
               s = [value[:-3], value[3:]]
               
          elif len(value) == 9:
               sort = main_[2][:-9]
               s = value[:3], value[3:6], value[-3:]
               
               del main_[2]
               main_.append(sort)
               
               main_[0] = main_[0] + f' {s[0]}'
               main_[1] = main_[1] + f' {s[1]}'
               main_[2] = main_[2] + f' {s[2]}'
               
               return '/'.join(main_)
               
          else:
               value = lesson.split(':')
               group = value[-1][:1]
               
               del value[-1]
               value.append(group)
               
               return ''.join(value)
                    
          del main_[1]       # ? Удаляю второй элемент списка с налепленными кабинетами
          main_.append(sort)       # ? Добаляю отсортированный второй элемент без кабинетов, только с номером группы
                    
          main_[0] = main_[0] + f' {s[0]}'
          main_[1] = main_[1] + f' {s[1]}'
               
          return '/'.join(main_)
     return lesson


async def find_day_int(int_day: int, class_: str):
     if int_day == 7: return True
     
     day = days[int_day - 1]
     data = await sh.get_json()
     
     classes = data[class_][day]
     output = f'День: {day}. Класс: {class_}'
     new = []
     
     value = time_1 if not classes[0].isspace() else time_2
     for i in classes:
          if not i.isspace():
               new.append(await sorted_text(i))
                                        
     for x in range(len(new)):
          output += f'\n\n{x + 1} урок. Время: {value[x]} \n {new[x]}'
          
     return markdown.hblockquote(output)


async def day_of_week(arg: str, id: int):
     class_ = await dtb.show_class_id(id)
     
     if not class_:
          return False
     
     if arg.isdigit() and int(arg) <= 7:
          return await find_day_int(int(arg), class_)
          
     else:
          return None


async def calls() -> str:
     output = '1 смена'
     for item in range(len(time_1)):
          output += f'\n{item + 1} урок: <b>{time_1[item]}</b>'
               
               
     output += '\n\n2 смена'
     for item in range(len(time_2)):
          output += f'\n{item + 1} урок: <b>{time_2[item]}</b>'
          
     return output


async def send_request() -> list:
     await asyncio.sleep(1)
     
     url = 'https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=ru'
     try:
          async with aiohttp.ClientSession() as session:
               async with session.get(url) as response:
                    data = await response.json()
     except Exception as ex:
          logger.error(ex)
          return []
     
     return [data['quoteText'], data['quoteAuthor']]


async def send_message_admin(message_text: str, chat_id: int, sender_name: str, id: int) -> None:
     bot = Bot(os.environ.get('TOKEN'))
     await bot.send_message(chat_id, text=f'{sender_name}. ID: {id} \n{message_text}')
     
     await bot.session.close()
     

async def send_message_one_user(message_text: str, id: int) -> None:
     bot = Bot(os.environ.get('TOKEN'))
     await bot.send_message(id, text=f'Admin \n{message_text}')
     
     await bot.session.close()
     
     
async def send_message_all_users(message_text: str) -> None:
     id_ = await dtb.show_all_id()
     bot = Bot(os.environ.get('TOKEN'))
     
     for items in id_:
          try:
               await bot.send_message(items[0], message_text)
               await bot.session.close()
               
          except Exception as ex:
               continue
     
     
     