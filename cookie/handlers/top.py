from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, InputMediaPhoto
from keyboards.kb import make_inlines_kb, make_inline_kb
from keyboards.kb import main_menu,funkci_menu,vidi_menu,predpochteniya_menu,tip_pitaniya_menu
import requests

from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State

from keyboards.kb import make_inlines_kb

router = Router()

class Top(StatesGroup):
    step_list = State()
    step = State()

@router.message(F.text== "🕓Свежие рецепты🕓")
async def top_10(message: types.Message, state):
    await state.clear()

    result = search_worker()
    await state.update_data(step_list=result)
    await state.update_data(step=0)

    text = (
        f"<b>{result[0][1]}</b>\n\n"
        f"Игредиенты для блюда:\n\n▪️{'\n▪️'.join(result[0][4])}"
    )
    
    await message.answer_photo(
        photo=result[0][2],
        caption=text,
        reply_markup=make_inlines_kb([
            ("Готовить", f"cooked_{result[0][0]}"),
            ("➡️", f"topstep_next")
        ], 2)
    )

@router.callback_query(F.data.startswith("topstep"))
async def topstep_callback(callback, state):
    where = callback.data.split("_")[-1]
    user_data = await state.get_data()

    if where == "next":
        step = user_data["step"] + 1
    elif where == "back":
        step = user_data["step"] - 1

    await state.update_data(step=step)

    user_data = await state.get_data()
    step_info = user_data["step_list"][step]

    text = (
        f"<b>{step_info[1]}</b>\n\n"
        f"Игредиенты для блюда:\n\n▪️{"\n▪️".join(step_info[4])}"
    )

    media = InputMediaPhoto(media=step_info[2], caption=text)

    if step == 10:
        keyboard = make_inlines_kb([
            ("⬅️", f"topstep_back"),
            ("Готовить", f"cooked_{step_info[0]}")
        ], 3)
    elif step == 0:
        keyboard = make_inlines_kb([
            ("Готовить", f"cooked_{step_info[0]}"),
            ("➡️", f"topstep_next"),
        ], 4)
    else:
        keyboard = make_inlines_kb([
            ("⬅️", f"topstep_back"),
            ("Готовить", f"cooked_{step_info[0]}"),
            ("➡️", f"topstep_next"),
        ], 3)

    await callback.message.edit_media(
        media=media,
        reply_markup=keyboard
    )

def _get_html():
    url = "https://www.povarenok.ru/recipes/?sort=date_create&order=desc"
    r = requests.get(url)
    r.encoding = 'windows-1251'  # указать правильную кодировку

    return r.text

def _html_process(html):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find_all('article', class_='item-bl')

    results = []
    for article in articles:
        # Название
        title_tag = article.find('h2')
        title = title_tag.get_text(strip=True) if title_tag else 'Нет названия'

        # Ссылка на рецепт
        url_tag = article.find("a")
        url_src = url_tag["href"] if url_tag else "Нет ссылки"

        # Ссылка на картинку
        img_tag = article.find('div', class_='m-img').find('img') if article.find('div', class_='m-img') else None
        img_src = img_tag['src'] if img_tag else 'Нет картинки'

        # Описание (первый <p>)
        desc_tag = article.find('p')
        description = desc_tag.get_text(strip=True) if desc_tag else 'Нет описания'

        # Основные продукты в списке
        ingr_spans = article.find('div', class_='ingr_fast')
        if ingr_spans:
            ingredients = [span.get_text(strip=True) for span in ingr_spans.find_all('span')]
        else:
            ingredients = []

        results.append((url_src, title, img_src, description, ingredients))
    return results

def search_worker():
    html = _get_html()
    return _html_process(html)


