from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import config
import telebot

from bd import add_to_airtable

bot = telebot.TeleBot(config.TOKEN)
print(config.TOKEN)

name = ""
username = ""
link = ""
city = ""
theme = ""
status = ""


@bot.message_handler(commands=['start', 'help'])
def start(message):
    print(message.from_user.first_name)
    if message.text == '/start':
        # TODO: Проверка на повторный ввод /start
        bot.send_message(message.chat.id,
                         'Привет!👋\nЯ Matching бот в Санкт-Петербурге 🤖 \n\nКаждую неделю я буду '
                         'предлагать вам для встречи интересного человека, случайно выбранного среди других '
                         'участников сообщества.\n\nДля старта ответьте на несколько вопросов.\n\n👉 Поехали 🚀​')
        bot.send_message(message.chat.id, '☕️ Напишите Имя и Фамилию')
        bot.register_next_step_handler(message, get_login)
    else:
        bot.send_message(message.from_user.id, 'Жми /start чтобы начать',
                         reply_markup=telebot.types.ReplyKeyboardRemove())


def get_login(message):
    # TODO: Проверка верно введенного Имя Фамилия
    global name
    global username
    name = message.text
    username = message.from_user.username
    choose_country(message)  # Next step


def choose_country(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    item1 = types.KeyboardButton("Санкт-Петербург")
    item2 = types.KeyboardButton("Москва")
    item3 = types.KeyboardButton("Другой город")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id,
                     '🌎 Выберите свой город.\n\nТак мы определим, где вы сможете встретиться с партнёром 🤝',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_link(message):
    global theme
    if message.text == "Дизайн" or message.text == "Разработка" or message.text == "Стартапы":
        theme = message.text
        choose(message)

    global city
    if message.text == "Санкт-Петербург":
        city = message.text
        bot.send_message(message.from_user.id,
                         '🤳 Пришлите ссылку на свой профиль в любой соц. сети,где есть наиболее подробная информация о '
                         'вас.\n\nТак вы сможете лучше узнать друг о друге до встречи. Можно поставить прочерк, '
                         'если не хотите ничего указывать.,',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, save_link)
        print('op srabotalo')
    elif message.text == "Москва" or message.text == "Другой":
        bot.send_message(message.from_user.id, "Этот город пока не подключен",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, choose_country)


def save_link(message):
    print('9999999999999999')
    global link
    link = message.text
    choose_theme(message)


def choose_theme(message):
    print('0000000000000000000000000000000000')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    item1 = types.KeyboardButton("Дизайн")
    item2 = types.KeyboardButton("Разработка")
    item3 = types.KeyboardButton("Стартапы")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id,
                     'Выберите свою предпочтительную дисциплину.',
                     reply_markup=markup)


def choose(message):
    print(add_to_airtable(name, username, link, city, theme, "Ready"))
    bot.send_message(message.chat.id,
                     'Получилось! 🙌\n\nТеперь вы — участник встреч 💪\n\nЧто дальше?\n\n1)  Каждый '
                     'понедельник мы будем присылать вашу пару для встречи в этот чат.\nНапишите партнеру в Telegram, '
                     'чтобы договориться о совместном походе на занятие.\nЕсли ваши предпочтения не совпали, '
                     'то вы можете просто выбраться на чашечку кофе.\nВремя и место вы выбираете сами.',
                     reply_markup=telebot.types.ReplyKeyboardRemove())


if __name__ == '__main__':
    bot.infinity_polling()
