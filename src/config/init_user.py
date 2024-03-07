import sqlite3

con = sqlite3.connect("sqlite.db")
cur = con.cursor()
cur.execute("CREATE TABLE user (id INTEGER NOT NULL,username VARCHAR(80) NOT NULL UNIQUE,email VARCHAR(120) NOT NULL,"
            "password VARCHAR(120) NOT NULL,role VARCHAR(120),PRIMARY KEY (id));")
cur.execute("INSERT INTO user VALUES('1', 'admin', 'admin@mail', 'admin', 'admin');")
con.commit()
res = cur.execute("select * from user")
print(res.fetchall())