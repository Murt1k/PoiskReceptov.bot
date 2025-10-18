from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove,InputMediaPhoto
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from keyboards.kb import main_menu,funkci_menu,vidi_menu,predpochteniya_menu,tip_pitaniya_menu
from services.get_recept import get_recept
from keyboards.kb import make_inlines_kb

from database import *

router = Router()

class Steps(StatesGroup):
    step_list = State()
    step = State()

# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply(
        'Этот бот предназначен для подбора рецептов и создания уникального рациона\n\n'
    )

    add_user(message.chat.id, message.chat.username)

    #add_user(message.chat.id, )

    await message.answer(
        "Меню:",
        reply_markup=funkci_menu()
    )

@router.message(F.text== "🏠В начало🏠")
async def V_nachalo(message: types.Message):

    await message.answer(
        "Меню:",
        reply_markup=funkci_menu()
    )

@router.message(F.text== "📋 Найти рецепт 📋")
async def vidi_receptov(message: types.Message):
    await message.reply(
        "Выберите нужную вам функцию"
    )
    await message.answer(
        "Меню:",
        reply_markup=funkci_menu()
    )


@router.callback_query(F.data.startswith("cooked_"))
async def cmd_command_cooked(callback: types.CallbackQuery,state):
    await state.clear()
    url = callback.data[7:]
    Ingridiens, steps = get_recept(url)
    Ingridiens = [str(Ingridiens[i-1]+" - "+Ingridiens[i])for i in range(1,len(Ingridiens),2)]
    Ingridiens = "\n".join(Ingridiens)

    await state.update_data(step_list=steps)
    await state.update_data(step=0)

    await callback.message.answer(
        f"Ингридиенты:\n\n{Ingridiens}",
        reply_markup=make_inlines_kb([
            ("➡️", f"move_next"),
        ],2)
    )

@router.callback_query(F.data.startswith("move"))
async def callback_move(callback: types.CallbackQuery, state):
    where = callback.data.split("_")[-1]

    user_data = await state.get_data()
    step_list = user_data["step_list"]
    step = user_data["step"]

    if where == "next":
        step = user_data["step"] + 1
    elif where == "back":
        step = user_data["step"] - 1
    await state.update_data(step=step)

    user_data = await state.get_data()
    step_text = user_data["step_list"][step]


    media = InputMediaPhoto(media=step_text[0], caption=step_text[1])

    if len(user_data["step_list"]) - 1 == step:
        keyboard = make_inlines_kb([
            ("⬅️", f"move_back")
        ],2)
    elif step == 0:
        keyboard = make_inlines_kb([
            ("➡️", f"move_next"),
        ],2)
    else:
        keyboard = make_inlines_kb([
            ("⬅️", f"move_back"),
            ("➡️", f"move_next"),
        ],2)

    await callback.message.edit_media(media=media, reply_markup=keyboard)

@router.message(Command("stat"))
async def cmd_stat(message: types.Message):
    if check_admins(message.chat.id):
        text = "Пользователи бота: \n\n"
        for i in get_all_username():
            text += "@" + i + "\n"

        await message.reply(
            text
        )
    else:    
        await message.reply(
            "Вы не админ!"
        )
