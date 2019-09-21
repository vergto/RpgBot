import telebot
import requests
import urllib.request
import sqlite3

bot = telebot.TeleBot('952476420:AAHOxzyLhPslDRyRMaxGY2YTZN-ZlGrpwIU')

@bot.message_handler(commands=['start'])
def start_message(message):
    async def process_start_command(message: types.Message):
        await message.reply("Привет!", reply_markup=kb.greet_kb)

   # bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

bot.polling()
