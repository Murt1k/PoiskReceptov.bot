import sqlite3

db = "db.db" # "./cookie/db.db"
conn = sqlite3.connect(db)
cur = conn.cursor()

def add_user(chat_id, username, role="user"):
	if not chat_id in get_all_user():
		cur.execute(
			"INSERT INTO users (id, username, role) VALUES (?, ?, ?);", 
			(chat_id, username, role)
		)
		conn.commit()

def get_all_user():
	cur.execute("SELECT id FROM users")
	result = cur.fetchall()

	return [i[0] for i in result]

def check_admins(chat_id):
	cur.execute("SELECT role FROM users WHERE id = ?", (chat_id,))
	result = cur.fetchall()

	if result[0][0] == "admin":
		return True
	return False

def get_all_username():
	cur.execute("SELECT username FROM users")
	result = cur.fetchall()

	return [i[0] for i in result]

def close_database():
	cur.close()