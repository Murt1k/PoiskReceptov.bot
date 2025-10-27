from aiogram import Router, F, types
from aiogram.types import Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from keyboards.kb import make_inlines_kb, make_inline_kb

from handlers.search_utils import *

router = Router()

class Search_key(StatesGroup):
    production = State()
    type_dish_key = State()
    exclude = State()
    step_list = State()
    step = State()
    page = State()

@router.message(F.text == "🔝По ключевым продуктам🔝")
async def search_key_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="🍽️Выберите тип блюда🍽️: ",
        reply_markup=make_inlines_kb([
            ("🍜Бульоны и супы🍜", "type_dish_key_2"),
            ("🍲Горячие🍲", "type_dish_key_6"),
            ("🍪Выпечка🍪", "type_dish_key_25"),
            ("🥫Соус🥫", "type_dish_key_23"),
            ("🥙Закуска🥙", "type_dish_key_15"),
            ("🥗Салат🥗", "type_dish_key_12"),
            ("🫕Каши🫕", "type_dish_key_55"),
            ("🍰Десерты🍰", "type_dish_key_30"),
            ("🥤Напитки🥤", "type_dish_key_19")
        ])
    )
    # Устанавливаем пользователю состояние "выбирает тип блюда"
    await state.set_state(Search_key.type_dish_key)

@router.callback_query(F.data.startswith("type_dish_key"))
async def cmd_command_type_dish(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(type_dish_key=callback.data)
    await callback.message.answer(
        "✅Напишите через запятую продукты, которые должны содержаться в блюде✅\n\nПишите вточности как в примере с уточнениями для лучшего подбора\n\n"
        "Например: мука пшеничкая, сыр козий, майонез, крупа гречневая"
    )

    await state.set_state(Search_key.production)
    await callback.answer()

@router.message(Search_key.production)
async def cmd_command_exclude(message: Message, state: FSMContext):
    product = message.text.lower().split(", ")
    await state.update_data(production=product)
    await message.answer(
        f"❌Напишите через запятую продукты, которые НЕ должны содержаться в блюде❌\n\nПишите вточности как в примере\n"
        f"Например: кунжут, свекла, майонез, чеснок",
        reply_markup=make_inlines_kb([
            ("➡️Пропустить➡️", "Pass")
        ])
    )
    # Переходим к состоянию "выбирает продукты"
    await state.set_state(Search_key.exclude)

async def update_state(page, state):
    user_data = await state.get_data()

    steps = search_worker(
        words=user_data["production"],
        type_dish=user_data["type_dish_key"].split("_")[-1],
        exclude=user_data["exclude"],
        function="keys_products",
        page=page
    )
    if steps == 404:
        return 404

    steps = user_data["step_list"] + steps

    await state.update_data(step_list=steps)
    await state.update_data(page=page)
    
@router.callback_query(F.data.startswith("Pass"))
@router.message(Search_key.exclude)
async def cmd_command_production(message, state: FSMContext):
    try:
        exclude = message.text.lower().split(", ")
    except:
        message = message.message
        exclude = ""

    await state.update_data(exclude=exclude)
    user_data = await state.get_data()

    steps = search_worker(
        words=user_data["production"],
        type_dish=user_data["type_dish_key"].split("_")[-1],
        exclude=user_data["exclude"],
        function="keys_products",
        page=1
    )

    if steps == 404:
        await message.answer(f"Ошибка!!!")
        return 
    
    await state.update_data(step_list=steps)
    await state.update_data(step=0)
    await state.update_data(page=1)

    user_data = await state.get_data()

    text = (
        f"<b>{user_data["step_list"][user_data["step"]][1]}</b>\n\n"
        f"Игредиенты для блюда:\n\n▪️{"\n▪️".join(user_data["step_list"][user_data["step"]][4])}"
    )

    await message.answer_photo(
        photo=user_data["step_list"][user_data["step"]][2], 
        caption=text,
        reply_markup=make_inlines_kb([
            ("Готовить", f"cooked_{user_data["step_list"][user_data["step"]][0]}"),
            ("➡️", f"step_next"),
        ], 2)
    )


@router.callback_query(F.data.startswith("step"))
async def callback_step(callback: types.CallbackQuery, state: FSMContext):

    where = callback.data.split("_")[-1]
    user_data = await state.get_data()
    if where == "next":
        step = user_data["step"] + 1
    elif where == "back":
        step = user_data["step"] - 1
    await state.update_data(step=step)

    user_data = await state.get_data()
    step_text = user_data["step_list"][step]

    text = (
        f"<b>{step_text[1]}</b>\n\n"
        f"Игредиенты для блюда:\n\n▪️{"\n▪️".join(step_text[4])}"
    )

    media = InputMediaPhoto(media=step_text[2], caption=text)

    if step == len(user_data["step_list"]) - 1:
        r = await update_state(user_data["page"]+1, state)
        if r == 404:
            await message.answer(f"Ошибка!!!")
            return

    if step == 100:
        keyboard = make_inlines_kb([
            ("⬅️", f"step_back"),
            ("Готовить", f"cooked_{step_text[0]}")
        ], 3)
    elif step == 0:
        keyboard = make_inlines_kb([
            ("Готовить", f"cooked_{step_text[0]}"),
            ("➡️", f"step_next"),
        ], 4)
    else:
        keyboard = make_inlines_kb([
            ("⬅️", f"step_back"),
            ("Готовить", f"cooked_{step_text[0]}"),
            ("➡️", f"step_next"),
        ], 3)

    await callback.message.edit_media(
        media=media, 
        reply_markup=keyboard
    )
