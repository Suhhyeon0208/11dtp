import sqlite3

db = sqlite3.connect('cars.db')
cursor = db.cursor()
sql = "SELECT * FROM car;"
cursor.execute(sql)
results = cursor.fetchall()
print(results)
#close the db
db.close()