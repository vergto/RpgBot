import telebot
import requests
import urllib.request
import sqlite3

bot = telebot.TeleBot('952476420:AAHOxzyLhPslDRyRMaxGY2YTZN-ZlGrpwIU')


@bot.message_handler(commands=['start'])
def start_message(message):
    start = telebot.types.ReplyKeyboardMarkup(True, False)
    itembtna = telebot.types.KeyboardButton('Бой ⚔')
    itembtnb = telebot.types.KeyboardButton('Профиль 🎫')
    itembtnc = telebot.types.KeyboardButton('Инвентарь 🎒')
    itembtnd = telebot.types.KeyboardButton('В гильдию 🏰')
    itembtne = telebot.types.KeyboardButton('Прокачать 🏅')
    start.row(itembtna, itembtnb)
    start.row(itembtnc, itembtnd, itembtne)
    bot.send_message(message.from_user.id, "Выбери действие:", reply_markup=start)

    # start.row('Бой')
    # start.row('Профиль')
    # start.row('Инвентарь')
    # start.row('Войти')
    # bot.send_message(message.from_user.id, 'Выбери действие', reply_markup=start)

bot.polling()

