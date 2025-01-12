import sqlite3,time

project = {}
obj = time.gmtime()
db = sqlite3.connect('index.db')
sql = db.cursor()
sql.execute('''CREATE TABLE IF NOT EXISTS projects (
project_day TEXT
)''')
db.commit()
user_plan = input("Your plane >")
user_data = input("Write when you want work with your project >")
project[(user_data)] = user_plan
print(project)
sql.execute('''SELECT project_day FROM projects''')
if sql.fetchone() is None:
    sql.execute('INSERT INTO projects FROM (?)', (project[(user_data)]))

db.close()