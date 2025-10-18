from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.kb import main_menu,funkci_menu,vidi_menu,predpochteniya_menu,tip_pitaniya_menu

router = Router()

@router.message(F.text== "⚙️ Настройки ⚙️")
async def settings(message: types.Message):
    await message.reply(
        'Функция в разработке'
    )
    '''await message.answer(
        "Меню:",
        reply_markup=predpochteniya_menu()
    )'''
    



