import sqlite3 as sql
from hashlib import sha256

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


delete_table()

create_table()

fill_table()
