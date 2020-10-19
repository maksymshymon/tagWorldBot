import telebot
import sqlite3

TOKEN = ''

DB = sqlite3.connect("db.db", check_same_thread=False)
cursor = DB.cursor()
bot = telebot.TeleBot(TOKEN)


def get_all_id():
    global DB, cursor
    request = "SELECT id FROM chat"
    result = cursor.execute(request).fetchall()
    return [i[0] for i in result]


def add_id_to_db(chat_id):
    global DB, cursor
    try:
        request = "INSERT INTO chat(id,users) VALUES(?,?)"
        cursor.execute(request, (chat_id, " "))
        DB.commit()
    except Exception as e:
        print(repr(e))


def get_users(chat_id):
    # print(user_id)
    global DB, cursor
    request = "SELECT users FROM chat WHERE id=?"
    cursor.execute(request, (chat_id,))
    result = cursor.fetchone()
    return result[0]


def set_users(chat_id, value):
    global DB, cursor
    request = "UPDATE chat SET users=? WHERE id=?"
    cursor.execute(request, (value, chat_id))
    DB.commit()


def get_countUsing(chat_id):
    # print(user_id)
    global DB, cursor
    request = "SELECT countUsing FROM chat WHERE id=?"
    cursor.execute(request, (chat_id,))
    result = cursor.fetchone()
    return result[0]

def set_countUsing(chat_id, value):
    global DB, cursor
    request = "UPDATE chat SET countUsing=? WHERE id=?"
    cursor.execute(request, (value, chat_id))
    DB.commit()


def get_countPeople(chat_id):
    # print(user_id)
    global DB, cursor
    request = "SELECT countPeople FROM chat WHERE id=?"
    cursor.execute(request, (chat_id,))
    result = cursor.fetchone()
    return result[0]


def set_countPeople(chat_id, value):
    global DB, cursor
    request = "UPDATE chat SET countPeople=? WHERE id=?"
    cursor.execute(request, (value, chat_id))
    DB.commit()

def get_countUsingGeneral():
    # print(user_id)
    global DB, cursor
    request = "SELECT countUsing FROM stats WHERE id=?"
    cursor.execute(request, (str(1),))
    result = cursor.fetchone()
    return result[0]

def set_countUsingGeneral(value):
    global DB, cursor
    request = "UPDATE stats SET countUsing=? WHERE id=?"
    cursor.execute(request, (value, str(1)))
    DB.commit()


def get_countPeopleGeneral():
    # print(user_id)
    global DB, cursor
    request = "SELECT countPeople FROM stats WHERE id=?"
    cursor.execute(request, (str(1),))
    result = cursor.fetchone()
    return result[0]


def set_countPeopleGeneral(value):
    global DB, cursor
    request = "UPDATE stats SET countPeople=? WHERE id=?"
    cursor.execute(request, (value, str(1)))
    DB.commit()


@bot.message_handler(commands=['start'])
def start(message):

    add_id_to_db(message.chat.id)
    bot.send_message(message.chat.id,
                     "<b>Справка по боту:</b>\n1. Используйте команду /tagworld , чтобы тегнуть людей из списка\n2. Чтобы добавить себя в список используйте команду /addme\n3. Чтобы удалить себя из списка, используйте команду /delme\n4. Тегать могут только администраторы",
                     parse_mode='html', reply_markup=None)


@bot.message_handler(commands=['addme'])
def addme(message):
    try:
        users = get_users(message.chat.id)
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
        set_users(message.chat.id, users)
    except Exception as e:
        bot.send_message(message.chat.id,
                         "Ошибка.",
                         parse_mode='html', reply_markup=None)




@bot.message_handler(commands=['delme'])
def delme(message):
    try:
        users = get_users(message.chat.id)
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
        set_users(message.chat.id, users)
    except Exception as e:
        bot.send_message(message.chat.id,
                         "Ошибка.",
                         parse_mode='html', reply_markup=None)


@bot.message_handler(commands=['tagworld'])
def tagworld(message):
    try:
        users = get_users(message.chat.id)
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
            set_countUsing(message.chat.id, int(get_countUsing(message.chat.id))+1)
            set_countPeople(message.chat.id, int(get_countPeople(message.chat.id))+len(users))

            set_countUsingGeneral(int(get_countUsingGeneral()) + 1)
            set_countPeopleGeneral(int(get_countPeopleGeneral()) + len(users))

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


DB = sqlite3.connect("db.db", check_same_thread=False)
cursor = DB.cursor()
bot.polling(none_stop=True)
