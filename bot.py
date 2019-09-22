import telebot
import requests
import urllib.request
import sqlite3

# Создаем базу данных
users = sqlite3.connect("users.db")
with users:
    cur = users.cursor()
    cur.execute("DROP TABLE IF EXISTS Users")
    cur.execute("CREATE TABLE Users(Id INT, UserName TEXT, Strength INT, intellect INT, Agility INT, "
                "Stamina INT, Luck INT)")
cur.close()


# git add .
# git commit -m "first commit"
# git push -u origin master

bot = telebot.TeleBot('952476420:AAHOxzyLhPslDRyRMaxGY2YTZN-ZlGrpwIU')


def hello(message):
    users = sqlite3.connect("users.db")
    name = message.from_user.first_name
    with users:
        cur = users.cursor()
        cur.execute("""INSERT INTO Users VALUES(?,?,?,?,?,?,?);""",
                    (str(message.from_user.id), str(name), str('5'), str('5'), str('5'), str('5'), str('5')))
    cur.close()

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
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
        rows = cur.fetchall()
    cur.close()
    if rows == []:
        bot.callback_query_handler(hello(message))

def users_list(message):
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users")
        rows = cur.fetchall()
        for row in rows:
            bot.send_message(message.from_user.id, str(row))



def users_window(message):
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
        rows = cur.fetchall()
        cur.close()
    if rows == []:
        bot.send_message(message.from_user.id, "Привет, вижу ты здесь впервые.")
    else:
        bot.send_message(message.from_user.id, "Профиль игрока: " + str(rows[0][1]) +"\n\n"\
                             "💪 Сила: " + str(rows[0][2]) +"\n"\
                             "📚 Интелект: " + str(rows[0][3]) +"\n"\
                             "🤸 ‍Ловкость: " + str(rows[0][4]) +"\n"\
                             "🧘 ‍Выносливость: " + str(rows[0][5]) +"\n"\
                             "🎯 Удача: " + str(rows[0][6]))

def users_up_stats(message):
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
        rows = cur.fetchall()
        cur.close()
    if rows == []:
        bot.send_message(message.from_user.id, "Привет, вижу ты здесь впервые, нажми /start")
    else:
        up_stats = telebot.types.ReplyKeyboardMarkup(True, False)
        itembtna = telebot.types.KeyboardButton('💪 Сила')
        itembtnb = telebot.types.KeyboardButton('📚 Интелект')
        itembtnc = telebot.types.KeyboardButton('🤸 ‍Ловкость')
        itembtnd = telebot.types.KeyboardButton('🧘 ‍Выносливость:')
        itembtne = telebot.types.KeyboardButton('🎯 Удача')
        up_stats.row(itembtna, itembtnb)
        up_stats.row(itembtnc, itembtnd, itembtne)
        bot.send_message(message.from_user.id,  "Что желаете прокачать " + str(rows[0][1]) +"?\n", reply_markup=up_stats)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет" or message.text == "привет":
        users = sqlite3.connect("users.db")
        with users:
            cur = users.cursor()
            cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
            rows = cur.fetchall()
        cur.close()
        if rows == []:
            bot.send_message(message.from_user.id, "Привет, вижу ты здесь впервые, нажми /start")
        else:
            bot.send_message(message.from_user.id, "Привет, " + str(rows[0][1]) + ", чем я могу тебе помочь?")
    elif message.text == "Пользователи" or message.text == "пользователи":
        bot.callback_query_handler(users_list(message))
    elif message.text == "Профиль" or message.text == "профиль" or message.text == "Профиль 🎫":
        bot.callback_query_handler(users_window(message))
    elif message.text == "Прокачать 🏅" or message.text == "Прокачать" or message.text == "прокачать":
        bot.callback_query_handler(users_up_stats(message))


    # start.row('Бой')
    # start.row('Профиль')
    # start.row('Инвентарь')
    # start.row('Войти')
    # bot.send_message(message.from_user.id, 'Выбери действие', reply_markup=start)

bot.polling()

