"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
from aiogram import Bot, Dispatcher, executor, types

import exceptions
import expenses
from categories import Categories


logging.basicConfig(level=logging.INFO)

API_TOKEN = "1442047970:AAG-LDhF3ZReMJhA5gsR77Kaf9C5ms3IxMc"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start', 'help', 'back'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Бот для учёта финансов 📝\n\n"
        'Добавить расход: "150 такси"'+"\n\n"
        "🔹 Сегодняшняя статистика: /today\n"
        "🔸 За текущий месяц: /month\n"
        "🔹 Последние внесённые расходы: /expenses\n"
        "🔸 Категории трат: /categories")


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись о расходе по её идентификатору"""
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)

    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Удалено!\n\n"
                             "Теперь расходов нет 😇"
                             "\n\nВернуться назад: /back")
        return

    last_expenses_rows = [
        f"{expense.amount} грн. на {expense.category_name} — нажми "
        f"/del{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = ("Удалено!\n\n"
                      "Последние сохранённые траты:\n\n* " + "\n\n* " \
                      .join(last_expenses_rows) + "\n\nВернуться назад: /back")
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """Отправляет список категорий расходов"""
    categories = Categories().get_all_categories()
    answer_message = "ℹ️ Категории трат:\n\n* " + \
                     ("\n* ".join([c.name + ' (' + ", ".join(c.aliases) + ')' for c in categories]) + "\n\nВернуться назад: /back")
    await message.answer(answer_message)


@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    """Отправляет статистику трат текущего месяца"""
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    """Отправляет последние несколько записей о расходах"""
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer('Расходы ещё не заведены 😏\n\nДобавить расход: "200 продукты"')
        return

    last_expenses_rows = [
        f"{expense.amount} грн. на {expense.category_name} — нажми "
        f"/del{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = "ℹ️ Последние сохранённые траты:\n\n* " + "\n\n* " \
        .join(last_expenses_rows) + "\n\nВернуться назад: /back"
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавляет новый расход"""
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлены траты {expense.amount} грн на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics()}\n\n"
        "Вернуться назад: /back")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
