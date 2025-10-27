from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from keyboards.kb import make_inlines_kb

router = Router()

'''
@router.message(F.text == "По имеющимся продуктам")
async def search_main_menu(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите тип блюда: ",
        reply_markup=make_inlines_kb([
            ("Завтрак", "type_dish_stock_Breakfast"),
            ("Горячее", "type_dish_stock_Main"),
            ("Салаты", "type_dish_stock_Salat"),
            ("Закуски", "type_dish_stock_Snack"),
            ("Десерт", "type_dish_stock_Dessert")
        ])
    )
    # Устанавливаем пользователю состояние "выбирает тип блюда"
    await state.set_state(Search.type_dish)

@router.callback_query(F.data.startswith("type_dish_stock"))
async def cmd_open_ticket(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(type_dish=callback.data)
    await callback.message.answer(
        "Напишите через запятую продукты, которые у вас есть\n\n"
        "Например: кунжут, свекла, майонез, чеснок"
    )
    # Переходим к состоянию "выбирает продукты"
    await state.set_state(Search.production)
    await callback.answer()  # Закрываем "часики" у callback

@router.message(Search.production)
async def type_ticket_chosen(message: Message, state: FSMContext):
    product = message.text.lower().split(", ")
    await state.update_data(production=product)
    user_data = await state.get_data()
    await message.answer(
        text=f'Вы выбрали: {user_data["production"]}. Тип блюда: {user_data["type_dish"]}'
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()
'''

@router.message(F.text== "По имеющимся продуктам")
async def settings(message: types.Message):
    await message.reply(
        'Функция в разработке))'
    )