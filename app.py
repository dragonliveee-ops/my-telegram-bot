import os
import asyncio
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Твой токен (вставлен)
TOKEN = "8902890841:AAH0Pyf3VKroU8KSfnSyjs7_ERY_D2BkDkI"

bot = Bot(token=TOKEN)
dp = Dispatcher()
app = Flask(__name__)

# --- Хендлеры ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="О нас")],
            [types.KeyboardButton(text="Контакты")],
            [types.KeyboardButton(text="Цены")]
        ],
        resize_keyboard=True
    )
    await message.answer("Привет! Я демо-бот. Выбери пункт меню:", reply_markup=keyboard)

@dp.message(lambda message: message.text == "О нас")
async def about(message: types.Message):
    await message.answer("Мы — учебный проект. Бот создан для портфолио.")

@dp.message(lambda message: message.text == "Контакты")
async def contacts(message: types.Message):
    await message.answer("Напиши @example (учебный контакт)")

@dp.message(lambda message: message.text == "Цены")
async def price(message: types.Message):
    await message.answer("Цена такого бота — от 400 ₽ под ключ.")

# --- Запуск бота в потоке ---
def run_bot():
    asyncio.run(dp.start_polling(bot))

@app.route('/')
def index():
    return "Telegram bot is running!"

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)