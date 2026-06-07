import os
import json
import requests
from flask import Flask, request

TOKEN = "8902890841:AAH0Pyf3VKroU8KSfnSyjs7_ERY_D2BkDkI"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    requests.post(BASE_URL + "sendMessage", json=payload)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text")
        if text == "/start":
            keyboard = {
                "keyboard": [["О нас"], ["Контакты"], ["Цены"]],
                "resize_keyboard": True
            }
            send_message(chat_id, "Привет! Я демо-бот. Выбери пункт меню:", keyboard)
        elif text == "О нас":
            send_message(chat_id, "Мы — учебный проект. Бот создан для портфолио.")
        elif text == "Контакты":
            send_message(chat_id, "Напиши @example (учебный контакт)")
        elif text == "Цены":
            send_message(chat_id, "Цена такого бота — от 400 ₽ под ключ.")
        else:
            send_message(chat_id, "Используй кнопки меню.")
    return "ok", 200

@app.route("/")
def index():
    return "Bot is running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
