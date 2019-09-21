import telebot
import requests
import urllib.request
import sqlite3

# Создаем базу данных
users = sqlite3.connect("users.db")
with users:
    cur = users.cursor()
    cur.execute("DROP TABLE IF EXISTS Users")
    cur.execute("CREATE TABLE Users(Id INT, UserName TEXT, Name TEXT)")
cur.close()

bot = telebot.TeleBot('952476420:AAHOxzyLhPslDRyRMaxGY2YTZN-ZlGrpwIU')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

def trans(message):
    eng_text=message.text
    token = 'trnsl.1.1.20190723T225100Z.9217a62b128c6cc4.a7fe8a8177be0ca3fcd368166bdc4e69a8002e11'
    url_trans = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    trans_option = {'key':token, 'lang':'en-ru', 'text': eng_text}
    webRequest = requests.get(url_trans, params = trans_option)
    webRequest.text
    rus_text= webRequest.text
    rus_text = rus_text[36:(len(rus_text)-3)]
    bot.send_message(message.from_user.id, rus_text)

def weath(message):
    city=message.text
    res = requests.get('http://api.openweathermap.org/data/2.5/find?q='+
                       city+'&type=like&APPID=d3f517bbd28897fbe8f51d1021673eca')
    data = res.json()
    try:
        if data['list'][0]['rain']:
            print('da')
            bot.send_message(message.from_user.id, 'конечно, на улице дождь, закончится через: '
                             + str(data['list'][0]['rain']['1h']) + ' час(ов)')
        else:
            bot.send_message(message.from_user.id, 'нет, сейчас без осадков')
    except:
        bot.send_message(message.from_user.id, "Ты ошибся в запросе. Попробуй ещё раз")

def kurs(message):
    from xml.etree import ElementTree as ET
    id_dollar = "R01235"
    id_evro = "R01239"
    valuta = ET.parse(urllib.request.urlopen("https://www.cbr-xml-daily.ru/daily.xml"))
    for line in valuta.findall('Valute'):
        id_v = line.get('ID')
        if id_v == id_dollar:
            rub_dollar = line.find('Value').text
        if id_v == id_evro:
            rub_evro = line.find('Value').text
    bot.send_message(message.from_user.id, 'доллар(USD): '+str(rub_dollar)+' руб')
    bot.send_message(message.from_user.id, 'евро(EUR): ' + str(rub_evro)+' руб')
    
def birth(message):
    try:
        god=int(message.text)-2010
        data = requests.get('https://apidata.mos.ru/v1/datasets/2008/rows?api_key=ba90057284f49996b0e222d987f357de')
        data=data.json()
        bot.send_message(message.from_user.id, 'всего родилось: '+str(data[god]['Cells']['TotalNumber']))
        bot.send_message(message.from_user.id, 'мальчиков: '+str(data[god]['Cells']['NumberOfBoys']))
        bot.send_message(message.from_user.id, 'девочек: '+str(data[god]['Cells']['NumberOfGirls']))
    except:
        bot.send_message(message.from_user.id, "Ты ошибся в запросе. Попробуй ещё раз")

def users_list(message):
    users = sqlite3.connect("users.db")
    with users:
        cur = users.cursor()
        cur.execute("SELECT * FROM Users")
        rows = cur.fetchall()
        for row in rows:
            bot.send_message(message.from_user.id, str(row))

def hello(message):
    users = sqlite3.connect("users.db")
    name = message.from_user.first_name
    with users:
        cur = users.cursor()
        cur.execute("""INSERT INTO Users VALUES(?,?,?);""",(str(message.from_user.id),str(name),str(message.text)))
    cur.close()

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if (message.text == "Привет" or message.text == "привет"):
        users = sqlite3.connect("users.db")
        with users:
            cur = users.cursor()
            cur.execute("SELECT * FROM Users WHERE Id="+str(message.from_user.id))
            rows = cur.fetchall()
        cur.close()
        if rows == []:
            bot.send_message(message.from_user.id, "Привет, вижу ты здесь впервые.")
            message = bot.send_message(message.from_user.id, "Как к тебе обращаться?")
            bot.register_next_step_handler(message, hello)
        else:
            bot.send_message(message.from_user.id, "Привет, " + str(rows[0][2]) + ", чем я могу тебе помочь?")
    elif (message.text == "/help" or message.text == "помощь" or message.text == "Помощь"):
        bot.send_message(message.from_user.id, 'Смотри что я могу: \n'\
        'Напиши мне: курс - я скажу текущий курс валют' \
        '\n брать ли зонт - скажу о текущей погоде \n' \
        'переведи - переведу текст\n'\
        'рождаемость - пришлю статистику рождаемости в Москве')
    elif (message.text == "переведи" or message.text == "Переведи"):
        message=bot.send_message(message.from_user.id, "Введи фразу")
        try:
            bot.register_next_step_handler(message, trans)
        except:
            bot.send_message(message.from_user.id, "Ты ошибся в запросе. Попробуй ещё раз")
    elif (message.text == "Брать ли мне завтра с собой зонтик?" or message.text == "зонт"
          or message.text == "Брать ли зонт" or message.text == "брать ли зонт" or message.text == "Зонт"):
        message = bot.send_message(message.from_user.id, "Введи город")
        try:
            bot.register_next_step_handler(message, weath)
        except:
            bot.send_message(message.from_user.id, "Ты ошибся в запросе. Попробуй ещё раз")
    elif (message.text == "курс валют" or message.text == "курс" or message.text == "Курс валют" or message.text == "Курс" ):
        try:
            bot.callback_query_handler(kurs(message))
        except:
            bot.send_message(message.from_user.id, "Ты ошибся в запросе. Попробуй ещё раз")
    elif (message.text == "рождаемость" or message.text == "Рождаемость"):
        message = bot.send_message(message.from_user.id, "Введи год")
        try:
            bot.register_next_step_handler(message, birth)
        except:
            bot.send_message(message.from_user.id, "Ты ошибся в запросе. Попробуй ещё раз")
    elif (message.text == "Пользователи" or message.text == "пользователи"):
        bot.callback_query_handler(users_list(message))
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
bot.polling()
