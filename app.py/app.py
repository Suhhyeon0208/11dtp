import sqlite3

db = sqlite3.connect("task7.db")
cursor = db.cursor()
sql = "SELECT * from task7;"
cursor.execute(sql)
result = cursor.fetchall()
print(results)
db.close()