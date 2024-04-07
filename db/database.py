import logging
import sqlite3 as sq

db = sq.connect("db/my_database.db")
cur = db.cursor()

'''
async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "user_id INTEGER, "
                "cart_id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS items("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT,"
                "desc TEXT, "
                "price TEXT, "
                "photo TEXT, "
                "brand TEXT)")
    db.commit()
'''


async def cmd_start_db(user_id, name):
    logging.info(msg=f"{name}")
    logging.info(msg=f"{user_id}")
    user = cur.execute("SELECT * FROM users WHERE user_id == {key}".format(key=user_id)).fetchone()
    print(user)
    if not user:
        logging.info(type(name))
        cur.execute(f"INSERT INTO users (username, user_id) VALUES (?,?)", (name, user_id))
        db.commit()

