import telebot
import sqlite3
import schedule
import time

TOKEN = ''

DB = sqlite3.connect("db.db", check_same_thread=False)
cursor = DB.cursor()
bot = telebot.TeleBot(TOKEN)


def get_countUsingGeneral():
    # print(user_id)
    global DB, cursor
    request = "SELECT countUsing FROM stats WHERE id=?"
    cursor.execute(request, (str(1),))
    result = cursor.fetchone()
    return result[0]


def get_countPeopleGeneral():
    # print(user_id)
    global DB, cursor
    request = "SELECT countPeople FROM stats WHERE id=?"
    cursor.execute(request, (str(1),))
    result = cursor.fetchone()
    return result[0]


def stats():
    bot.send_message(000000000,
                     "Users tagged: <b>"+str(get_countPeopleGeneral())+"</b>\nTag used: <b>"+str(get_countUsingGeneral())+"</b>",
                     parse_mode='html', reply_markup=None)


schedule.every().day.at("20:00").do(stats)
DB = sqlite3.connect("db.db", check_same_thread=False)
cursor = DB.cursor()
while True:
    schedule.run_pending()
    time.sleep(10)
