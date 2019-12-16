import telebot
import sqlite3
bot = telebot.TeleBot('952476420:AAHOxzyLhPslDRyRMaxGY2YTZN-ZlGrpwIU')


# Кнопка назад, возвращает стартовый интерфейс
def rearwards(message):
    rearw = telebot.types.ReplyKeyboardMarkup(True, False)
    itembtna = telebot.types.KeyboardButton('Бой ⚔')
    itembtnb = telebot.types.KeyboardButton('Профиль 🎫')
    itembtnd = telebot.types.KeyboardButton('Путешествовать‍')
    itembtne = telebot.types.KeyboardButton('Прокачать 🏅')
    rearw.row(itembtna, itembtnb)
    rearw.row(itembtnd, itembtne)
    bot.send_message(message.from_user.id, "Вы вернулись в стартовое меню", reply_markup=rearw)


# Окно пользователя, показывает характеристики персонажа
def users_window(message):
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
        rows = cur.fetchall()
        cur.close() 
    if not rows:
        bot.send_message(message.from_user.id, "Привет, вижу ты здесь впервые, нажми /start")
    else:
        bot.send_message(message.from_user.id, "Профиль игрока: " + str(rows[0][1]) + "\n" \
                                                "Уровень: " + str(rows[0][8]) + "   " \
                                                + str(rows[0][9]) + "/" + str(rows[0][10]) + "\n\n" \
                                                "🗺 Карта: /map \n\n" \
                                                "❤ HP: " + str(rows[0][11]) + "\n" \
                                                "🔪 DMG: " + str(rows[0][12]) + "\n\n" \
                                                "💪 Сила: " + str(rows[0][2]) + "\n" \
                                                "📚 Интелект: " + str(rows[0][3]) + "\n" \
                                                "🤸 ‍Ловкость: " + str(rows[0][4]) + "\n" \
                                                "🧘 ‍Выносливость: " + str(rows[0][5]) + "\n" \
                                                "🎯 Удача: " + str(rows[0][6]) + "\n\n" \
                                                 "💰 Золото: " + str(rows[0][7]))


# Кнопки перемещения в зависимости от местоположения
def go_throw_map(message):
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
        rows = cur.fetchall()
    if not rows:
        bot.send_message(message.from_user.id, "Привет, вижу ты здесь впервые, нажми /start")
    else:
        up_stats = telebot.types.ReplyKeyboardMarkup(True, False)
        if rows[0][13] == 0:
            itembtnf = telebot.types.KeyboardButton('Деревня')
            itembtna = telebot.types.KeyboardButton('Забытые руины')
            itembtnb = telebot.types.KeyboardButton('Озеро чудовищ')
            itembtnc = telebot.types.KeyboardButton('Огненный грот')
            itembtnd = telebot.types.KeyboardButton('Не путешествовать')
            up_stats.row(itembtnf)
            up_stats.row(itembtna)
            up_stats.row(itembtnb)
            up_stats.row(itembtnc)
            up_stats.row(itembtnd)
        elif rows[0][13] == 1:
            itembtna = telebot.types.KeyboardButton('Вернуться в город')
            itembtnb = telebot.types.KeyboardButton('Заброшенная башня')
            up_stats.row(itembtna)
            up_stats.row(itembtnb)
        elif rows[0][13] == 2:
            itembtna = telebot.types.KeyboardButton('Вернуться в город')
            itembtnb = telebot.types.KeyboardButton('Оазис')
            up_stats.row(itembtna)
            up_stats.row(itembtnb)
        elif rows[0][13] == 3:
            itembtna = telebot.types.KeyboardButton('Вернуться в город')
            itembtnb = telebot.types.KeyboardButton('Логово Кракена')
            up_stats.row(itembtna)
            up_stats.row(itembtnb)
        elif rows[0][13] == 4:
            itembtna = telebot.types.KeyboardButton('Вернуться в город')
            itembtnb = telebot.types.KeyboardButton('Логово Дракона')
            up_stats.row(itembtna)
            up_stats.row(itembtnb)
        elif rows[0][13] >= 5:
            itembtna = telebot.types.KeyboardButton('Вернуться в город')
            up_stats.row(itembtna)
        bot.send_message(message.from_user.id, "Куда желаете пойти?", reply_markup=up_stats)

        cur.close()


def go_map(message):
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
        rows = cur.fetchall()
        if message.text == "Деревня":
            cur.execute("UPDATE Users SET MAP = 1 WHERE  Id=" + str(message.from_user.id))
            bot.send_message(message.from_user.id, "Вы перешли в деревню")
            bot.callback_query_handler(rearwards(message))
        elif message.text == "Забытые руины":
            cur.execute("UPDATE Users SET MAP = 2 WHERE  Id=" + str(message.from_user.id))
            bot.send_message(message.from_user.id, "Вы перешли в Забытые руины")
            bot.callback_query_handler(rearwards(message))
        elif message.text == "Озеро чудовищ":
            cur.execute("UPDATE Users SET MAP = 3 WHERE  Id=" + str(message.from_user.id))
            bot.send_message(message.from_user.id, "Вы перешли в Озеро чудовищ")
            bot.callback_query_handler(rearwards(message))
        elif message.text == "Огненный грот":
            cur.execute("UPDATE Users SET MAP = 4 WHERE  Id=" + str(message.from_user.id))
            bot.send_message(message.from_user.id, "Вы перешли в Огненный грот")
            bot.callback_query_handler(rearwards(message))
        elif message.text == "Вернуться в город":
            cur.execute("UPDATE Users SET MAP = 0 WHERE  Id=" + str(message.from_user.id))
            bot.send_message(message.from_user.id, "Вы вернулись в город")
            bot.callback_query_handler(rearwards(message))
        elif message.text == "Заброшенная башня":
            cur.execute("UPDATE Users SET MAP = 5 WHERE  Id=" + str(message.from_user.id))
            bot.send_message(message.from_user.id, "Вы перешли в Заброшенную башню")
            bot.callback_query_handler(rearwards(message))
        elif message.text == "Оазис":
            cur.execute("UPDATE Users SET MAP = 6 WHERE  Id=" + str(message.from_user.id))
            bot.send_message(message.from_user.id, "Вы перешли в Оазис")
            bot.callback_query_handler(rearwards(message))
        elif message.text == "Логово Кракена":
            cur.execute("UPDATE Users SET MAP = 7 WHERE  Id=" + str(message.from_user.id))
            bot.send_message(message.from_user.id, "Вы перешли в Логово Кракена")
            bot.callback_query_handler(rearwards(message))
        elif message.text == "Логово Дракона":
            cur.execute("UPDATE Users SET MAP = 8 WHERE  Id=" + str(message.from_user.id))
            bot.send_message(message.from_user.id, "Вы перешли в Логово Дракона")
            bot.callback_query_handler(rearwards(message))
        cur.close()
