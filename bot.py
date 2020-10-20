import telebot
import db

TOKEN = '_________________'


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    db.add_id_to_db(message.chat.id)
    bot.send_message(message.chat.id,
                     "<b>Справка по боту:</b>\n1. Используйте команду /tagworld , чтобы тегнуть людей из списка\n2. Чтобы добавить себя в список используйте команду /addme\n3. Чтобы удалить себя из списка, используйте команду /delme\n4. Тегать могут только администраторы",
                     parse_mode='html', reply_markup=None)


@bot.message_handler(commands=['addme'])
def addme(message):
    try:
        users = db.get_users(message.chat.id)
        if users is None or len(users) == 0:
            users = ''
        users = users.split()
        users = [int(i) for i in users]
        if message.from_user.username:
            if message.from_user.id not in users:
                users.append(message.from_user.id)
                bot.send_message(message.chat.id,
                                 message.from_user.username + " добавлен",
                                 parse_mode='html', reply_markup=None)
            else:
                bot.send_message(message.chat.id,
                                 "Вы уже есть в списке 😉",
                                 parse_mode='html', reply_markup=None)
        else:
            bot.send_message(message.chat.id,
                             "Добавьте в настройках своего профиля имя пользователя, чтобы быть в списке 🙂",
                             parse_mode='html', reply_markup=None)
        users = ' '.join([str(elem) for elem in users])
        db.set_users(message.chat.id, users)
    except Exception as e:
        bot.send_message(message.chat.id,
                         "Ошибка.",
                         parse_mode='html', reply_markup=None)




@bot.message_handler(commands=['delme'])
def delme(message):
    try:
        users = db.get_users(message.chat.id)
        if users is None or len(users) == 0:
            users = ''
        users = users.split()
        users = [int(i) for i in users]
        if message.from_user.id in users:
            users.remove(message.from_user.id)
            bot.send_message(message.chat.id,
                         message.from_user.username + " удален",
                         parse_mode='html', reply_markup=None)
        else:
            bot.send_message(message.chat.id,"Вас нет в списке. Чтобы добавить себя в список нажмите \n/addme@tagworldbot",
                             parse_mode='html', reply_markup=None)
        users = ' '.join([str(elem) for elem in users])
        db.set_users(message.chat.id, users)
    except Exception as e:
        bot.send_message(message.chat.id,
                         "Ошибка.",
                         parse_mode='html', reply_markup=None)


@bot.message_handler(commands=['tagworld'])
def tagworld(message):
    try:
        users = db.get_users(message.chat.id)
        if users is None or len(users) == 0:
            users = ''
        users = users.split()
        users = [int(i) for i in users]
        s = bot.get_chat_member(message.chat.id, message.from_user.id).status
        s = str(s)
        if s == 'member':
            bot.send_message(message.chat.id,
                             "У тебя нет прав.",
                             parse_mode='html', reply_markup=None)
        elif len(users) > 0:
            p = ""
            db.set_countUsing(message.chat.id, int(db.get_countUsing(message.chat.id)) + 1)
            db.set_countPeople(message.chat.id, int(db.get_countPeople(message.chat.id)) + len(users))

            db.set_countUsingGeneral(int(db.get_countUsingGeneral()) + 1)
            db.set_countPeopleGeneral(int(db.get_countPeopleGeneral()) + len(users))

            for s in users:
                if s != "":
                    p = p + '\n@' + bot.get_chat_member(message.chat.id, s).user.username
            bot.send_message(message.chat.id,
                             p,
                             parse_mode='html', reply_markup=None)
        else:
            bot.send_message(message.chat.id, "Список пустой. Чтобы добавить себя в список нажмите \n/addme@tagworldbot", parse_mode='html', reply_markup=None)
    except Exception as e:
        bot.send_message(message.chat.id,
                         "Ошибка.",
                         parse_mode='html', reply_markup=None)


db.setup()
bot.polling(none_stop=True)
