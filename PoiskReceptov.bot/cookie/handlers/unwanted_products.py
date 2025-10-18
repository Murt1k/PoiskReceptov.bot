from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards.kb import main_menu,funkci_menu,vidi_menu,predpochteniya_menu,tip_pitaniya_menu

router = Router()

'''class Search(StatesGroup):
    production = State()
    type_dish = State()




@router.message(F.text== "Нежелательные продукты")
async def unwanted_products(message: types.Message,state):

    await message.answer(
        "Напишите через запятую продукты, которые нежелательны в вашем блюде\n\n"
        "Например: кунжут, свекла, майонез, чеснок"
    )
    # Переходим к состоянию "выбирает продукты"
    await state.set_state(Search.production)


@router.message(Search.production)
async def type_ticket_chosen(message: Message, state: FSMContext):
    product = message.text.lower().split(", ")
    await state.update_data(production=product)
    user_data = await state.get_data()
    await message.answer(
        text=f'Вы выбрали: {user_data["production"]}. '
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()'''