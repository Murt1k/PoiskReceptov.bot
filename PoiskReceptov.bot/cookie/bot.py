import asyncio
import logging
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import aioschedule
from config_reader import config
from handlers import cmd_commands,foodtype,top,key_products,search
from services import mailing
from keyboards.kb import make_inline_kb
import antyflood
from antyflood import AntiFloodMiddleware
from database import *

from aiogram.types import URLInputFile



# Объект бота
bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)
dp = Dispatcher()
dp.message.middleware(AntiFloodMiddleware())

    

async def start_mailing():

    users = get_all_user()

    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text="🥘🔔Ежедневня рассылка вкусного рецепта🔔🥘")

            recept = mailing.search_worker()[0]

            photo = URLInputFile(recept[2])
            t = (
            f"<b>{recept[1]}</b>\n\n"
            f"Игредиенты для блюда:\n\n▪️{"\n▪️".join(recept[4])}")

            await bot.send_photo(
                chat_id=user_id,
                photo=photo, 
                caption=t,
                reply_markup=make_inline_kb("Готовить", f"cooked_{recept[0]}")
        )
        except Exception:
            pass 

async def scheduler():
    aioschedule.every().day.at("13:00").do(start_mailing)  # рассылка каждый день в 9 утра
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


# Запуск процесса поллинга новых апдейтов
async def main():
    asyncio.create_task(scheduler())
	# Логгирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Диспетчер
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_routers(
        cmd_commands.router,
        foodtype.router,
        top.router,
        key_products.router,
        antyflood.router,
        search.router
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())