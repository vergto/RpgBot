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
                "Stamina INT, Luck INT, Gold INT, LVL INT, LVL_OP INT, LVL_NEED_OP INT)")
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
        cur.execute("""INSERT INTO Users VALUES(?,?,?,?,?,?,?,?,?,?,?);""",
                    (str(message.from_user.id), str(name), str('5'), str('5'), str('5'), str('5'), str('5'),
                     str('1000'), str('1'), str('0'), str('100')))
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
        bot.send_message(message.from_user.id, "Привет, вижу ты здесь впервые, нажми /start")
    else:
        bot.send_message(message.from_user.id, "Профиль игрока: " + str(rows[0][1]) + "\n" \
                                                "Уровень: " + str(rows[0][8]) + "   "\
                                                + str(rows[0][9]) + "/" + str(rows[0][10]) + "\n\n" \
                                                "💪 Сила: " + str(rows[0][2]) + "\n" \
                                                "📚 Интелект: " + str(rows[0][3]) + "\n" \
                                                "🤸 ‍Ловкость: " + str(rows[0][4]) + "\n" \
                                                "🧘 ‍Выносливость: " + str(rows[0][5]) + "\n" \
                                                "🎯 Удача: " + str(rows[0][6]) + "\n\n" \
                                                "💰 Золото: " + str(rows[0][7]))


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
        itembtnd = telebot.types.KeyboardButton('🧘 ‍Выносливость')
        itembtne = telebot.types.KeyboardButton('🎯 Удача')
        itembtnf = telebot.types.KeyboardButton('Назад')
        up_stats.row(itembtna, itembtnb, itembtnc)
        up_stats.row(itembtnd, itembtne, itembtnf)
        bot.send_message(message.from_user.id, "Стоимость прокачки: " + str(100 * rows[0][8]) + "💰")
        bot.send_message(message.from_user.id, "Что желаете прокачать " + str(rows[0][1]) + "?\n",
                         reply_markup=up_stats)


def rearwards(message):
    rearw = telebot.types.ReplyKeyboardMarkup(True, False)
    itembtna = telebot.types.KeyboardButton('Бой ⚔')
    itembtnb = telebot.types.KeyboardButton('Профиль 🎫')
    itembtnc = telebot.types.KeyboardButton('Инвентарь 🎒')
    itembtnd = telebot.types.KeyboardButton('В гильдию 🏰')
    itembtne = telebot.types.KeyboardButton('Прокачать 🏅')
    rearw.row(itembtna, itembtnb)
    rearw.row(itembtnc, itembtnd, itembtne)
    bot.send_message(message.from_user.id, "Вы вернулись в стартовое меню", reply_markup=rearw)


def users_up_stats_inc(message):
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
        rows = cur.fetchall()
        price_stats_inc = 100 * rows[0][8]
        if rows[0][7] >= price_stats_inc:
            if message.text == "💪 Сила" or message.text == "Сила":
                type_stat = "Strength"
            elif message.text == "📚 Интелект" or message.text == "Интелект":
                type_stat = "intellect"
            elif message.text == "🤸 ‍Ловкость" or message.text == "‍Ловкость":
                type_stat = "Agility"
            elif message.text == "🧘 ‍Выносливость" or message.text == "‍Выносливость":
                type_stat = "Stamina"
            elif message.text == "🎯 Удача" or message.text == "Удача":
                type_stat = "Luck"
            cur.execute("UPDATE Users SET " + type_stat + "=" + type_stat + "+1 WHERE  Id=" + str(message.from_user.id))
            cur.execute("UPDATE Users SET Gold = Gold-" + str(price_stats_inc) + " WHERE  Id=" + str(message.from_user.id))
            bot.send_message(message.from_user.id, "Выбранная характеристика повысилась")
            bot.callback_query_handler(rearwards(message))
        else:
            bot.send_message(message.from_user.id, "Вам не хватает денег для прокачки характеристики")
            bot.callback_query_handler(rearwards(message))
    cur.close()


def battle(message):
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
        rows = cur.fetchall()
        cur.close()
    if not rows:
        bot.send_message(message.from_user.id, "Привет, вижу ты здесь впервые, нажми /start")
    else:
        bot.send_message(message.from_user.id, "на вас напал")


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
    elif message.text == "Назад" or message.text == "назад":
        bot.callback_query_handler(rearwards(message))
    elif message.text == "💪 Сила" or message.text == "Сила":
        bot.callback_query_handler(users_up_stats_inc(message))
    elif message.text == "📚 Интелект" or message.text == "Интелект":
        bot.callback_query_handler(users_up_stats_inc(message))
    elif message.text == "🤸 ‍Ловкость" or message.text == "‍Ловкость":
        bot.callback_query_handler(users_up_stats_inc(message))
    elif message.text == "🧘 ‍Выносливость" or message.text == "‍Выносливость":
        bot.callback_query_handler(users_up_stats_inc(message))
    elif message.text == "🎯 Удача" or message.text == "Удача":
        bot.callback_query_handler(users_up_stats_inc(message))
    elif message.text == "Бой ⚔" or message.text == "Бой":
        bot.callback_query_handler(battle(message))


bot.polling()
