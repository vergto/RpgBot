import telebot
import sqlite3
bot = telebot.TeleBot('952476420:AAHOxzyLhPslDRyRMaxGY2YTZN-ZlGrpwIU')


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
                                                "❤ HP: " + str(rows[0][11]) + "\n" \
                                                "🔪 DMG: " + str(rows[0][12]) + "\n\n" \
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
    if not rows:
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