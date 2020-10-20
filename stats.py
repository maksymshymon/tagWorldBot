import telebot
import db
import schedule
import time


TOKEN = '_____________________'

bot = telebot.TeleBot(TOKEN)



def stats():
    bot.send_message(-00000000,
                     "Users tagged: <b>" + str(db.get_countPeopleGeneral()) + "</b>\nTag used: <b>" + str(
                         db.get_countUsingGeneral()) + "</b>",
                     parse_mode='html', reply_markup=None)


schedule.every().day.at("20:00").do(stats)
db.setup()
while True:
    schedule.run_pending()
    time.sleep(10)
