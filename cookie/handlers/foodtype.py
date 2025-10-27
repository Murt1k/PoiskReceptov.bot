from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.kb import main_menu,funkci_menu,vidi_menu,predpochteniya_menu,tip_pitaniya_menu

router = Router()


@router.message(F.text== "Ваш тип питания")
async def DostupnieProdukti_receptov(message: types.Message):
    await message.answer(
        "Меню:",
        reply_markup=tip_pitaniya_menu()
    )
