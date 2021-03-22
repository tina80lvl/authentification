# Задача:
# Сделать API с возможностью авторизации пользователя и получения информации о
# нем только после успешной авторизации. Должны быть 3 endpoint'а: login (вводим
# логин и пароль, при успехе выдает токен), logout (делает токен
# недействительным) и user (при действующем токене выдает информацию о
# пользователе, имя, фамилию и дату рождения). Сделанный проект надо выгрузить в
# репозиторий на Github.
#
# Требования к функционалу:
# - если логин/пароль неправильные - выводим ошибку
# - одновременная поддержка нескольких сессий пользователя
# - защита от брутфорса (подбора пароля)
#
# Требования к коду:
# - нативный код без использования ФРЕЙМВОРКОВ, БИБЛИОТЕК
# - простая реализация логики
#
# Требования к БД:
# - простая и понятная структура данных
# - использование индексов
# - не хранить пароли в базе в открытом виде

import sqlite3 as sql
import time
import uuid
from hashlib import sha256

class Person:
    def __init__(self, name, surname, birth):
        self.name = name
        self.surname = surname
        self.birth = birth

    def print_info(self):
        print('Name: ', self.name, '\nSurname: ', self.surname, '\nBirthday: ', self.birth)


class Session:
    def __init__(self):
        self.logins = dict()

    def validate(self, login, password):
        # one request per second
        if login in self.logins and time.time() - self.logins[login] < 1000:
                return []
        self.logins[login] = time.time()
        con = sql.connect('test.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM 'people' WHERE login = ? AND password = ?", (login, sha256(password.encode('utf-8')).hexdigest(),))
            result = cur.fetchall()
            return result

    def login1(self):
        login = input('Enter Login: ')
        password = input('Enter Password: ')
        res = self.validate(login, password)
        if res == []:
            print('❌Invalid login/password!')
            return ''
        con = sql.connect('test.db')
        with con:
            cur = con.cursor()
            token = login + str(time.time())
            cur.execute("INSERT INTO logininfo VALUES (?, ?, ?)", (str(uuid.uuid4()).replace('-',''), res[0][0], token))
            con.commit()
            print('✅Logged in.')
            return token

    def logout1(self, token):
        con = sql.connect('test.db')
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM logininfo WHERE token = ?", (token,))
            con.commit()
            print('⬆️Logged out.')

    def user(self, token):
        con = sql.connect('test.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM 'people' WHERE person_id = (SELECT person_id FROM 'logininfo' WHERE token =?)", (token,))
            res = cur.fetchall()
            if res == []:
                print('❌No active token!')
            else:
                print('Name: ', res[0][1], '\nSurname: ', res[0][2], '\nBirthday: ', res[0][3])


def delete_table():
    con = sql.connect('test.db')
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE `people` ")
        cur.execute("DROP TABLE `logininfo` ")
        con.commit()
        print(con)


def create_table():
    con = sql.connect('test.db')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS `people` (`person_id` VARCHAR PRIMARY KEY, `name` VARCHAR, `surname` VARCHAR, `birthday` VARCHAR, `login` VARCHAR UNIQUE NOT NULL, `password` VARCHAR) ")
        cur.execute("CREATE TABLE IF NOT EXISTS `logininfo` (`session_id` VARCHAR PRIMARY KEY, `person_id` INTEGER REFERENCES `people` (`person_id`), 'token' VARCHAR )")
        con.commit()
        print(con)


def fill_table():
    con = sql.connect('test.db')
    with con:
        cur = con.cursor()
        u1 = ('sdjfu4-ld', 'Tina', 'Smirnova', '25-08-1998', 'tina', sha256('troll'.encode('utf-8')).hexdigest())
        u2 = ('kf93bdkkd', 'Ilya', 'Nesterenko', '17-09-1999', 'illusha', sha256('password'.encode('utf-8')).hexdigest())
        u3 = ('dljfc-sbd', 'God', 'Smith', '01-01-0', 'god', sha256('hatezeus'.encode('utf-8')).hexdigest())

        cur.execute("INSERT INTO people VALUES (?, ?, ?, ?, ?, ?)", u1)
        cur.execute("INSERT INTO people VALUES (?, ?, ?, ?, ?, ?)", u2)
        cur.execute("INSERT INTO people VALUES (?, ?, ?, ?, ?, ?)", u3)

        con.commit()
        print(con)

# delete_table()
create_table()

# uncomment for the first run
# fill_table()

# valid example
session = Session()
tok1 = session.login1()
session.user(tok1)
session.logout1(tok1)

# invalid token
tok2 = session.login1()
session.user('invalid_token')
session.logout1(tok2)

# equal logins for one user
tok3 = session.login1()
tok4 = session.login1()
session.user(tok3)
session.user(tok4)
session.logout1(tok3)
session.user(tok4)
session.logout1(tok4)
