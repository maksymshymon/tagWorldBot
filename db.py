import sqlite3

DB = sqlite3.connect("db.db", check_same_thread=False)
cursor = DB.cursor()

def setup():
    global DB, cursor
    DB = sqlite3.connect("db.db", check_same_thread=False)
    cursor = DB.cursor()

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