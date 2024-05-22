
import aiosqlite

from data_pack.shedule import get_json
from data_pack import commands_ as cmd


async def create_database() -> None:
     async with aiosqlite.connect('/data/bot.db') as db:
          await db.execute("""CREATE TABLE IF NOT EXISTS users(
               id INT,
               name STR,
               clsroom STR
               )""")
          await db.commit()
          
          
          
async def start_database(id: int, name: str) -> None:
     async with aiosqlite.connect('/data/bot.db') as db:
          exists = await db.execute("SELECT name FROM users WHERE id = ?", [id])
          exists = await exists.fetchone()
          
          if not exists:
               await db.execute("INSERT INTO users(id, name) VALUES(?, ?)", [id, name])
               await db.commit()
               
               return True


async def ancet_me_database(id: int):
     async with aiosqlite.connect('/data/bot.db') as db:
          exists = await db.execute("SELECT clsroom FROM users WHERE id = ?", [id])
          exists = await exists.fetchone()
          
          if not exists[0]:
               return None
     
          else:
               exists = await db.execute("SELECT * FROM users WHERE id = ?", [id])
               exists = await exists.fetchone()

               return f'''ID: <b>{exists[0]}</b> \nИмя: <b>{exists[1]}</b> \nКласс: <b>{exists[2]}</b>'''
          
   
          
async def new_clsroom_database(text: str, id: int):
     async with aiosqlite.connect('/data/bot.db') as db:
          await db.execute("UPDATE users SET clsroom = ? WHERE id = ?", [text, id])
          await db.commit()
     return True
     
          
          
async def remove_me_database(text: str, id: int):
     async with aiosqlite.connect('/data/bot.db') as db:
          exists = await db.execute("SELECT clsroom FROM users WHERE id = ?", [id])
          exists = await exists.fetchone()
          
          if not exists[0]:
               return None
          
          else:
               return await new_clsroom_database(text, id)
          
          
          
async def show_today_database(id: int):
     async with aiosqlite.connect('/data/bot.db') as db:
          exists = await db.execute("SELECT clsroom FROM users WHERE id = ?", [id])
          exists = await exists.fetchone()
          
          if not exists[0]:
               return False
          
     data_json = await get_json()
     out = await cmd.show_today(data_json, exists[0])
     
     return out
          
          
     
async def show_tomorrow_database(id: int):
     async with aiosqlite.connect('/data/bot.db') as db:
          exists = await db.execute("SELECT clsroom FROM users WHERE id = ?", [id])
          exists = await exists.fetchone()
          
          if not exists[0]:
               return False
          
     data_json = await get_json()
     out = await cmd.show_tomorrow(data_json, exists[0])
     
     return out


async def show_admin_users():
     async with aiosqlite.connect('/data/bot.db') as db:
          exists = await db.execute("SELECT * FROM users")
          exists: tuple = await exists.fetchall()
          
     out = ''
     count = 0
     
     for user_ in exists:
          count += 1
          out += f'Name: {user_[1]}; ID: {user_[0]}; Class: {user_[2]}\n'
          
     return [out, count]


async def show_all_id():
     async with aiosqlite.connect('/data/bot.db') as db:
          exists = await db.execute("SELECT id FROM users")
          exists = await exists.fetchall()
          
     return exists


async def show_class_id(id: int) -> str:
     async with aiosqlite.connect('/data/bot.db') as db:
          exists = await db.execute("SELECT clsroom FROM users WHERE id = ?", [id])
          exists = await exists.fetchone()
          
     return exists[0]
          