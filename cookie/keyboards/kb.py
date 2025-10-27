from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def make_inline_kb(text: str, callback_data: str) -> InlineKeyboardMarkup:
	"""
	Функиця возвращает инлайн-кнопку с callback data

	:param text: str. Текст кнопки

	:param callback_data: str. callback_data from InlineKeyboard

	:return: InlineKeyboardMarkup
	"""
	builder = InlineKeyboardBuilder()

	builder.add(
		types.InlineKeyboardButton(
			text=text,
			callback_data=callback_data
		)
	)

	return builder.as_markup()

def make_column_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
	"""
	Создаёт реплай-клавиатуру с кнопками в один столбец
	:param items: список текстов для кнопок
	:return: объект реплай-клавиатуры
	"""
	keyboard = [[KeyboardButton(text=item)] for item in items]
	return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def main_menu() -> ReplyKeyboardMarkup:
	kb = [
		[KeyboardButton(text="📋 Найти рецепт 📋")]]
		
	return ReplyKeyboardMarkup(
		keyboard=kb,
		resize_keyboard=True,
		input_field_placeholder="Выберите действие"
	)

def funkci_menu() -> ReplyKeyboardMarkup:
	kb = [
		[KeyboardButton(text="🔝По ключевым продуктам🔝")],
		[KeyboardButton(text="🕓Свежие рецепты🕓")],
		[KeyboardButton(text="🔎Поиск по названию🔎")],
		[KeyboardButton(text="🏠В начало🏠")]]

	return ReplyKeyboardMarkup(
		keyboard=kb,
		resize_keyboard=True,
		input_field_placeholder="Выберите действие"
	)

def vidi_menu() -> ReplyKeyboardMarkup:
	kb = [
		[KeyboardButton(text="Соус")],
		[KeyboardButton(text="Холодная закуска")],
		[KeyboardButton(text="Горячая закуска")],
		[KeyboardButton(text="Основное блюдо")],
		[KeyboardButton(text="Суп")],
		[KeyboardButton(text="Десерт")],
		[KeyboardButton(text="В начало")]]
	
	return ReplyKeyboardMarkup(
		keyboard=kb,
		resize_keyboard=True,
		input_field_placeholder="Выберите действие"
	)

def predpochteniya_menu() -> ReplyKeyboardMarkup:
	kb = [
		[KeyboardButton(text="Нежелательные продукты")],
		[KeyboardButton(text="Ваш тип питания")],
		[KeyboardButton(text="В начало")]]
	return ReplyKeyboardMarkup(
		keyboard=kb,
		resize_keyboard=True,
		input_field_placeholder="Выберите действие"
	)

def tip_pitaniya_menu() -> ReplyKeyboardMarkup:
	kb = [
		[KeyboardButton(text="Худею")],
		[KeyboardButton(text="Веган")],
		[KeyboardButton(text="Вегатарианец")],
		[KeyboardButton(text="Мясоед")],
		[KeyboardButton(text="В начало")]]
	return ReplyKeyboardMarkup(
		keyboard=kb,
		resize_keyboard=True,
		input_field_placeholder="Выберите действие"
	)

def make_inlines_kb(kb: list[tuple], row_width=1) -> InlineKeyboardMarkup:
	"""
	Принимает список кортежей, где 1 элемент - текст кнопки, 2 - callback_data

	row_width - количество столбцов
	"""
	builder = InlineKeyboardBuilder()

	for i in kb:
		builder.add(
			types.InlineKeyboardButton(
				text=i[0],
				callback_data=i[1]
			)
		)

	builder.adjust(row_width)

	return builder.as_markup()


