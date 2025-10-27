import sqlite3

db = "d2b.db" # "./cookie/db.db"
conn = sqlite3.connect(db)
cur = conn.cursor()

def create_database():
	cur.execute('''
		CREATE TABLE users (
		    id INTEGER PRIMARY KEY UNIQUE NOT NULL,
		    username TEXT UNIQUE NOT NULL,
		    role TEXT DEFAULT 'user' NOT NULL
		)
	''')

	conn.commit()
	conn.close()

create_database()