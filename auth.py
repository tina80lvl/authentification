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
        if login in self.logins and time.time() - self.logins[login] < 1:
            print('❌Too many attempts!')
            return []
        self.logins[login] = time.time()
        con = sql.connect('test.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM 'people' WHERE login = ? AND password = ?", (login, sha256(password.encode('utf-8')).hexdigest(),))
            result = cur.fetchall()
            return result

    def if_token_exist(self, token):
        con = sql.connect('test.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM 'people' WHERE person_id = (SELECT person_id FROM 'logininfo' WHERE token = ?)", (token,))
            res = cur.fetchall()
            return res


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
            print('✅Logged in. Token: ', token)
            return token


    def logout1(self, token):
        if self.if_token_exist(token) == []:
            print('❌No active token!')
            return

        con = sql.connect('test.db')
        with con:
            cur = con.cursor()
            t = cur.execute("DELETE FROM logininfo WHERE token = ?", (token,))
            con.commit()
            print('⬆️Logged out.')


    def user(self, token):
        res = self.if_token_exist(token)
        if res == []:
            print('❌No active token!')
        else:
            print('Name: ', res[0][1], '\nSurname: ', res[0][2], '\nBirthday: ', res[0][3])


# ----------------------------------- USAGE ------------------------------------


def print_usage():
    print('Please type one of the following options:\n1 : for logging in\n2 : for logging out\n3 : to get user information.\n0 : interrupt session\n')


print_usage()
session = Session()
while True:
    option = input('Input option: ')
    if option == '1':
        token = session.login1()
    elif option == '2':
        token = input('Enter token: ')
        session.logout1(token)
    elif option == '3':
        token = input('Enter token: ')
        session.user(token)
    elif option == '0':
        break
    else:
        print('❌Invalid option!')
        print_usage()
