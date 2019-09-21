import telebot
import requests
import urllib.request
import sqlite3

bot = telebot.TeleBot('952476420:AAHOxzyLhPslDRyRMaxGY2YTZN-ZlGrpwIU')


# bot.send_message(message.chat.id, 'Привет, ты написал мне /start')
@bot.message_handler(commands=['start'])
def start_message(message):
    start = telebot.types.ReplyKeyboardMarkup(True, False)
    start.row('Бой')
    start.row('Профиль')
    start.row('Инвентарь')
    start.row('Войти')
    bot.send_message(message.from_user.id, 'Выбери действие', reply_markup=start)

bot.polling()

