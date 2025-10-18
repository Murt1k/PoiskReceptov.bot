from aiogram import Router, F, types
from aiogram.types import Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from keyboards.kb import make_inlines_kb, make_inline_kb

from handlers.search_utils import *

router = Router()
"""
[
    (
        'https://www.povarenok.ru/recipes/show/87699/', 
        'Пампушки к борщу за 20 минут', 
        'https://www.povarenok.ru/data/cache/2014apr/03/30/707106_80557-330x220x.jpg', 
        'Категория:ВыпечкаИзделия из тестаБулочки', 
        ['Вода', 'Сахар', 'Масло подсолнечное', 'Соль', 'Дрожжи', 'Ванильный сахар', 'Мука пшеничная']
    ), 
]
"""

class Search(StatesGroup):
    text = State()
    posts = State()
    step = State()
    page = State()


@router.message(F.text == "🔎Поиск по названию🔎")
async def search_(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(  
        "Напишите то что вы ищите\n\n"
        "Например: борщ от тети Нюси"
    )

    # Переходим к состоянию "выбирает продукты"
    await state.set_state(Search.text)

async def update_state_serach(page, state):
    user_data = await state.get_data()

    steps = search_worker(
        words=user_data["text"],
        function="search",
        page=page
    )

    steps = user_data["posts"] + steps

    await state.update_data(posts=steps)
    await state.update_data(page=page)


@router.message(Search.text)
async def search_callback(message: Message, state: FSMContext):
    text = message.text.split()
    result = search_worker(words=text, function="search")
    
    await state.update_data(text=text)
    await state.update_data(posts=result)
    await state.update_data(step=0)
    await state.update_data(page=1)

    data = await state.get_data()
    data = data["posts"][data["step"]]

    t = (
        f"<b>{data[1]}</b>\n\n"
        f"Игредиенты для блюда:\n\n▪️{"\n▪️".join(data[4])}"
    )

    await message.answer_photo(
        photo=data[2], 
        caption=t,
        reply_markup=make_inlines_kb([
            ("Готовить", f"cooked_{data[0]}"),
            ("➡️", f"right_next"),
        ], 2)
    )

@router.callback_query(F.data.startswith("right"))
async def callback_step(callback: types.CallbackQuery, state: FSMContext):

    where = callback.data.split("_")[-1]
    user_data = await state.get_data()

    if where == "next":
        step = user_data["step"] + 1
    elif where == "back":
        step = user_data["step"] - 1
    await state.update_data(step=step)

    data = await state.get_data()
    page = data["page"]
    data = data["posts"]

    text = (
        f"<b>{data[step][1]}</b>\n\n"
        f"Игредиенты для блюда:\n\n▪️{"\n▪️".join(data[step][4])}"
    )

    media = InputMediaPhoto(media=data[step][2], caption=text)

    if step == len(data) - 1:
        await update_state_serach(page+1, state)

    if step == 100:
        keyboard = make_inlines_kb([
            ("⬅️", f"right_back"),
            ("Готовить", f"cooked_{data[step][0]}"),
        ], 3)
    elif step == 0:
        keyboard = make_inlines_kb([
            ("Готовить", f"cooked_{data[step][0]}"),
            ("➡️", f"right_next"),
        ], 4)
    else:
        keyboard = make_inlines_kb([
            ("⬅️", f"right_back"),
            ("Готовить", f"cooked_{data[step][0]}"),
            ("➡️", f"right_next"),
        ], 3)

    await callback.message.edit_media(
        media=media, 
        reply_markup=keyboard
    )

