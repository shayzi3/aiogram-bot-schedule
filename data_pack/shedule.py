
import ujson
import aiofiles



days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
time_1 = ['08:30 - 09:10', '09:15 - 09:55', '10:00 - 10:40', '10:55 - 11:35', '11:50 - 12:30', '12:40 - 13:20', '13:30 - 14:10', '14:25 - 15:05']  
time_2 = ['13:30 - 14:10', '14:25 - 15:05', '15:20 - 16:00', '16:05 - 16:45', '16:50 - 17:30', '17:35 - 18:15']


async def get_json() -> dict:
     path = 'ParsSchedule/data.json'
     
     async with aiofiles.open(path, 'r', encoding='utf-8') as f:
          return ujson.loads(await f.read())


               