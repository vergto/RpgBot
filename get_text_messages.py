import sqlite3
import telebot
import bmenu
from bot import users_list, users_up_stats, users_up_stats_inc, battle

bot = telebot.TeleBot('952476420:AAHOxzyLhPslDRyRMaxGY2YTZN-ZlGrpwIU')


class Get_text(object):
    # реакция бота на текс путем проверки полученного сообщения
    @bot.message_handler(content_types=['text'])
    def __init__(self, message):
        if message.text == "Привет" or message.text == "привет":
            users = sqlite3.connect("users.db")
            with users:
                cur = users.cursor()
                cur.execute("SELECT * FROM Users WHERE Id=" + str(message.from_user.id))
                rows = cur.fetchall()
            cur.close()
            if not rows:
                bot.send_message(message.from_user.id, "Привет, вижу ты здесь впервые, нажми /start")
            else:
                bot.send_message(message.from_user.id, "Привет, " + str(rows[0][1]) + ", чем я могу тебе помочь?")
        elif message.text == "Пользователи" or message.text == "пользователи":
            bot.callback_query_handler(users_list(message))
        elif message.text == "Профиль" or message.text == "профиль" or message.text == "Профиль 🎫":
            bot.callback_query_handler(bmenu.users_window(message))
        elif message.text == "Прокачать 🏅" or message.text == "Прокачать" or message.text == "прокачать":
            bot.callback_query_handler(users_up_stats(message))
        elif message.text == "Назад" or message.text == "назад" or message.text == "Не путешествовать":
            bot.callback_query_handler(bmenu.rearwards(message))
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
        elif message.text == "Путешествовать" or message.text == "путешествовать":
            bot.callback_query_handler(bmenu.go_throw_map(message))
        elif message.text == "Деревня" or message.text == "Забытые руины" or message.text == "Озеро чудовищ" \
                or message.text == "Огненный грот" \
                or message.text == "Вернуться в город" or message.text == "Заброшенная башня" or message.text == "Оазис" \
                or message.text == "Логово Кракена" or message.text == "Логово Дракона":
            bot.callback_query_handler(bmenu.go_map(message))
