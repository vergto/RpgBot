import telebot
import requests
import urllib.request
import sqlite3

bot = telebot.TeleBot('952476420:AAHOxzyLhPslDRyRMaxGY2YTZN-ZlGrpwIU')


# bot.send_message(message.chat.id, 'Привет, ты написал мне /start')
@bot.message_handler(commands=['start'])
def start_message(message):
    start = telebot.types.ReplyKeyboardMarkup(True, False)
    start.row('Wunderlist')
    start.add('Telegraph')
    start.row('Погода')
    start.insert('Контакты')
    bot.send_message(message.from_user.id, 'Выбери сервис', reply_markup=start)

bot.polling()

