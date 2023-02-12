import sqlite3

connection = sqlite3.connect('database.db')

with open('scheme.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("insert into items (title, description, priority) values (?, ?, ?)",
            ("First task", "Description for first task", 1))

cur.execute("insert into items (title, description, priority) values (?, ?, ?)",
            ("Second task", "Description for second task", 2))

cur.execute("insert into items (title, description, priority) values (?, ?, ?)",
            ("Third task", "Description for third task", 3))

cur.execute("insert into items (title, description, priority) values (?, ?, ?)",
            ("Forth task", "Description for forth task", 4))

cur.execute("insert into items (title, description, priority) values (?, ?, ?)",
            ("Fifth task", "Description for fifth task", 5))

connection.commit()
connection.close()
