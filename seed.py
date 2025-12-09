import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM images")
db.execute("DELETE FROM reviews")
db.execute("DELETE FROM themes")
db.execute("DELETE FROM category")
db.execute("DELETE FROM poems")
db.execute("DELETE FROM users")

user_count = 1000
poem_count = 10**5
review_count = 10**6


for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
               ["user" + str(i), "secret"])


for i in range(1, poem_count + 1):
    user_id = random.randint(1, user_count)
    db.execute("""INSERT INTO poems (title, content, published, user_id)
                  VALUES (?, ?, date('now'), ?)""",
               ["runo" + str(i), "sisältö" + str(i), user_id])

for i in range(1, review_count + 1):
    user_id = random.randint(1, user_count)
    poem_id = random.randint(1, poem_count)
    rating = random.randint(1, 10)
    db.execute("""INSERT INTO reviews (poem_id, user_id, rating, comment, date)
                  VALUES (?, ?, ?, ?, date('now'))""",
               [poem_id, user_id, rating, "kommentti" + str(i)])

db.commit()
db.close()