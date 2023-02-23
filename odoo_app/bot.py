import xmlrpc.client
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv, find_dotenv
from os import getenv


BUTTON_ALL_MESSAGES = "Получить все сообщения"
START_MESSAGE = """
Напишите 'Получить все сообщения', чтобы получить сообщения с сервера или 
отправьте любой другой текст, чтобы создать на сервере сообщение с этим текстом
"""
NO_MESSAGES = "В базе нет сообщений"


load_dotenv(find_dotenv())
URL = getenv("URL")
DB = getenv("DB")
USER = getenv("ODOO_USER")
PASSWORD = getenv("PASSWORD")


def start_bot(token: str) -> None:
    bot = TeleBot(token)
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = KeyboardButton(BUTTON_ALL_MESSAGES)
    markup.add(button)

    @bot.message_handler(commands=["start", "help"])
    def send_start_message(message):
        bot.send_message(
            chat_id=message.chat.id, text=START_MESSAGE, reply_markup=markup
        )

    @bot.message_handler(func=lambda message: True)
    def echo_buttons(message):
        if message.text == BUTTON_ALL_MESSAGES:
            messages = get_messages()

            if messages == []:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=NO_MESSAGES,
                    reply_markup=markup,
                )

            for mess in messages:
                bot.send_message(
                    chat_id=message.chat.id, text=mess, reply_markup=markup
                )

        else:
            save_message(message.text)
            bot.send_message(
                chat_id=message.chat.id, text="Сохранено", reply_markup=markup
            )

    bot.infinity_polling()


def get_messages() -> list:
    common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(URL))
    uid = common.authenticate(DB, USER, PASSWORD, {})
    models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(URL))
    messages = models.execute_kw(
        DB,
        uid,
        PASSWORD,
        "bot.messages",
        "search_read",
        [[]],
    )
    return [item["message"] for item in messages]


def save_message(message: str) -> None:
    common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(URL))
    uid = common.authenticate(DB, USER, PASSWORD, {})
    models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(URL))
    models.execute_kw(
        DB,
        uid,
        PASSWORD,
        "bot.messages",
        "create",
        [{"message": message}],
    )
