import telebot
import sqlite3
import bmenu
from rand_nps import *
from get_text_messages import *

# Создаем базу данных
users = sqlite3.connect("users.db")
with users:
    cur = users.cursor()
    cur.execute("DROP TABLE IF EXISTS Users")
    cur.execute("CREATE TABLE Users(Id INT, UserName TEXT, Strength INT, intellect INT, Agility INT, "
                "Stamina INT, Luck INT, Gold INT, LVL INT, LVL_OP INT, LVL_NEED_OP INT, HP INT, DMG INT, MAP INT)")
cur.close()

# git add .
# git commit -m "first commit"
# git push -u origin master

bot = telebot.TeleBot('952476420:AAHOxzyLhPslDRyRMaxGY2YTZN-ZlGrpwIU')


# Создание БД с данными о персонаже
def hello(message):
    users = sqlite3.connect("users.db")
    name = message.from_user.first_name
    with users:
        cur = users.cursor()
        cur.execute("""INSERT INTO Users VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?);""",
                    (str(message.from_user.id), str(name), str('5'), str('5'), str('5'), str('5'), str('5'),
                     str('1000'), str('1'), str('0'), str('100'), str('100'), str('10'), str('0')))
    cur.close()


# инициализация и вывод стартовых кнопок
@bot.message_handler(commands=['start'])
def start_message(message):
    start = telebot.types.ReplyKeyboardMarkup(True, False)
    itembtna = telebot.types.KeyboardButton('Бой ⚔')
    itembtnb = telebot.types.KeyboardButton('Профиль 🎫')
    itembtnd = telebot.types.KeyboardButton('Путешествовать')
    itembtne = telebot.types.KeyboardButton('Прокачать 🏅')
    start.row(itembtna, itembtnb)
    start.row(itembtnd, itembtne)
    bot.send_message(message.from_user.id, "Выбери действие:", reply_markup=start)
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
        rows = cur.fetchall()
    cur.close()
    if not rows:
        bot.callback_query_handler(hello(message))


# Вывод всех пользователей и их данных
def users_list(message):
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users")
        rows = cur.fetchall()
        for row in rows:
            bot.send_message(message.from_user.id, str(row))


# Кнопки предлагающие на выбор одну из прокачиваемых характеристик
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


# Функция повышения онной характеристики
def users_up_stats_inc(message):
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
        rows = cur.fetchall()
        type_stat = ""
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
        if type_stat != "" and rows[0][7] >= price_stats_inc:
            if type_stat == "Strength":
                cur.execute(
                    "UPDATE Users SET " + type_stat + "=" + type_stat + "+1 WHERE  Id=" + str(message.from_user.id))
                cur.execute(
                    "UPDATE Users SET Gold = Gold-" + str(price_stats_inc) + " WHERE  Id=" + str(message.from_user.id))
                cur.execute("UPDATE Users SET HP = HP+5 WHERE  Id=" + str(message.from_user.id))
                cur.execute("UPDATE Users SET DMG = DMG+2 WHERE  Id=" + str(message.from_user.id))
                bot.send_message(message.from_user.id, "Выбранная характеристика повысилась")
                bot.callback_query_handler(bmenu.rearwards(message))
            elif type_stat == "Stamina":
                cur.execute(
                    "UPDATE Users SET " + type_stat + "=" + type_stat + "+1 WHERE  Id=" + str(message.from_user.id))
                cur.execute(
                    "UPDATE Users SET Gold = Gold-" + str(price_stats_inc) + " WHERE  Id=" + str(message.from_user.id))
                cur.execute("UPDATE Users SET HP = HP+10 WHERE  Id=" + str(message.from_user.id))
                bot.send_message(message.from_user.id, "Выбранная характеристика повысилась")
                bot.callback_query_handler(bmenu.rearwards(message))
            elif type_stat == "Agility":
                cur.execute(
                    "UPDATE Users SET " + type_stat + "=" + type_stat + "+1 WHERE  Id=" + str(message.from_user.id))
                cur.execute(
                    "UPDATE Users SET Gold = Gold-" + str(price_stats_inc) + " WHERE  Id=" + str(message.from_user.id))
                cur.execute("UPDATE Users SET DMG = DMG+3 WHERE  Id=" + str(message.from_user.id))
                bot.send_message(message.from_user.id, "Выбранная характеристика повысилась")
                bot.callback_query_handler(bmenu.rearwards(message))
            elif type_stat == "Luck" or type_stat == "intellect":
                cur.execute(
                    "UPDATE Users SET " + type_stat + "=" + type_stat + "+1 WHERE  Id=" + str(message.from_user.id))
                cur.execute(
                    "UPDATE Users SET Gold = Gold-" + str(price_stats_inc) + " WHERE  Id=" + str(message.from_user.id))
                bot.send_message(message.from_user.id, "Выбранная характеристика повысилась")
                bot.callback_query_handler(bmenu.rearwards(message))
        else:
            bot.send_message(message.from_user.id, "Вам не хватает ❌денег❌ для прокачки характеристики")
            bot.callback_query_handler(bmenu.rearwards(message))
    cur.close()


# Рандомный монстр в зависимости от локации
# def rand_battle_monster(message):
#    users = sqlite3.connect("users.db")
#    with users:
#        cur = users.cursor()
#       cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
#       rows = cur.fetchall()
#        R = Rand_monster(rows[0][13])
#  return R.get_rand_monster()


# процесс повышения уровня персонажа
def lvl_up_hero(fight_logs_battle, monster_lvl, message):
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
        rows = cur.fetchall()
        experience_lvl = round((monster_lvl - rows[0][8] + 1) + (rows[0][10] / 100 * random.randint(3, 5)))
        fight_logs_battle = fight_logs_battle + "\nполучено опыта: " + str(experience_lvl)
        cur.execute(
            "UPDATE Users SET LVL_OP = LVL_OP+" + str(experience_lvl) + " WHERE  Id=" + str(message.from_user.id))
        lvl_up_flag = 0
        if (rows[0][9] + experience_lvl) >= rows[0][10]:
            cur.execute(
                "UPDATE Users SET LVL_OP = LVL_OP-" + str(rows[0][10]) + " WHERE  Id=" + str(message.from_user.id))
            cur.execute("UPDATE Users SET LVL_NEED_OP = LVL_NEED_OP*4 WHERE  Id=" + str(message.from_user.id))
            cur.execute("UPDATE Users SET LVL = LVL+1 WHERE  Id=" + str(message.from_user.id))
            cur.execute("UPDATE Users SET HP = HP+20 WHERE  Id=" + str(message.from_user.id))
            cur.execute("UPDATE Users SET DMG = DMG+5 WHERE  Id=" + str(message.from_user.id))
            fight_logs_battle = fight_logs_battle + "\n🎊🎊Ваш уровень повышен🎊🎊 \nЗдоровье увеличено на 20❤ и урон " \
                                                    "увеличен на 5🔪 "
            fight_logs_battle = fight_logs_battle + "\nВаш уровень: " + str(rows[0][8] + 1) + "   " \
                                + str(rows[0][9] + experience_lvl - rows[0][10]) + "/" + str(rows[0][10] * 4)
            lvl_up_flag = 1
        if lvl_up_flag == 0:
            fight_logs_battle = fight_logs_battle + "\nВаш уровень: " + str(rows[0][8]) + "   " \
                                + str(rows[0][9] + experience_lvl) + "/" + str(rows[0][10])
        gold_plus = round(monster_lvl * random.randint(1, 15))
        cur.execute("UPDATE Users SET Gold = Gold+" + str(gold_plus) + " WHERE  Id=" + str(message.from_user.id))
        fight_logs_battle = fight_logs_battle + "\nполучено: " + str(rows[0][7]) + "+" + str(gold_plus) + " золота💰"
        bot.send_message(message.from_user.id, fight_logs_battle)
    cur.close()


# Создание уровня и HP босса в зависимости от локации
def fight_battle_monster(fight_logs_battle, type_monster_battle, message):
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
        rows = cur.fetchall()
        cur.close()
    monster_lvl = round(rows[0][8] * random.randint(1, 3)) + rows[0][13]
    monster_hp = monster_lvl * random.randint(10, 20)
    if rows[0][13] == 7:
        monster_hp = monster_hp + 10000
    if rows[0][13] == 8:
        monster_hp = monster_hp + 20000
    hero_hp = rows[0][11]
    first_hit = round((rows[0][3] + rows[0][4] + rows[0][6]) / 3) - 1
    fight_logs_battle = fight_logs_battle + str(rows[0][1]) + ": " + str(hero_hp) + "❤ / " + str(
        type_monster_battle) + " " \
                        + str(monster_lvl) + " уровня: " + str(monster_hp) + "❤ \n\n"
    if first_hit > monster_lvl:
        flagg = 1
        fight_logs_battle = fight_logs_battle + str(rows[0][1]) + " Заметил монстра первым\n"
    else:
        flagg = 0
        fight_logs_battle = fight_logs_battle + "Герой не заметил подкрадывающегося монстра\n"
    while monster_hp >= 1 and hero_hp >= 1:
        hero_dmg = round(rows[0][12] * random.random() * 4)
        monster_dmg = round(50 + monster_lvl * random.random() * 4)
        if flagg == 1:
            flagg = 0
            monster_hp = monster_hp - hero_dmg
            fight_logs_battle = fight_logs_battle + str(rows[0][1]) + " ⚔ " + str(type_monster_battle) \
                                + " нанося " + str(hero_dmg) + " урона\n❤ у монстра осталось " + str(monster_hp) + "\n"
        elif flagg == 0:
            flagg = 1
            hero_hp = hero_hp - monster_dmg
            fight_logs_battle = fight_logs_battle + str(type_monster_battle) + " ⚔ героя нанося " \
                                + str(monster_dmg) + " урона\n❤ у героя осталось " + str(hero_hp) + "\n"
    if monster_hp <= 0 and hero_hp >= 1:
        fight_logs_battle = fight_logs_battle + "\n🎊Герой победил🎊"
        lvl_up_hero(fight_logs_battle, monster_lvl, message)
    elif hero_hp <= 0 and monster_hp >= 1:
        fight_logs_battle = fight_logs_battle + "\n☠Герой проиграл☠"
        bot.send_message(message.from_user.id, fight_logs_battle)


# Начало генерации битвы, на данном этапе подбирается монстр и сообщение передается след. функции
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
        R = Rand_monster(rows[0][13])
        type_monster_battle = R.get_rand_monster()
        fight_logs_battle = "на вас напал " + str(type_monster_battle) + "\n"
        fight_battle_monster(fight_logs_battle, type_monster_battle, message)


# Картинка карты мира
@bot.message_handler(commands=['map'])
def karta(message):
    bot.send_photo(message.from_user.id, photo=open('Map.jpg', 'rb'))


G = Get_text(massege)

bot.polling()
