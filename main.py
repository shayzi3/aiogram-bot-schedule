import asyncio
import os

from aiogram import Bot, Dispatcher
from loguru import logger

from handlers import user_commands, bot_commands, ancet, admin_commands
from data_pack.database_ import create_database
            

async def main() -> None:
     await create_database()
     logger.info('Bot is ready!')
     
     bot = Bot(os.environ.get('TOKEN'))
     dp = Dispatcher()
     
     dp.include_routers(
          user_commands.router,
          ancet.router,
          admin_commands.router,
          bot_commands.router
         
     )
     
     await bot.delete_webhook(drop_pending_updates=True)
     await dp.start_polling(bot)
     
     
if __name__ == '__main__':
     asyncio.run(main())
     