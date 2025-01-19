import sqlite3
from datetime import datetime, timedelta
from itertools import count


import telebot

project_bd = {}
project_time = None
project_name = None
db = sqlite3.connect('index.db')
sql = db.cursor()
sql.execute('''CREATE TABLE IF NOT EXISTS projects (
    project TEXT
)''')

class Planner:
    def proj(self, message):
        from bot import bot
        global project_time

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(30):
            time = datetime.now() + timedelta(days=i)
            item = telebot.types.KeyboardButton(time.strftime("%Y-%m-%d"))
            markup.add(item)

        bot.send_message(message.chat.id, "Выберите дату", reply_markup=markup)


    def handle_date_selection(self, message):
        global project_time
        from bot import bot
        print(f"Message text: {message.text}")
        if message.text != 'planers':
            project_time = message.text
            print(f"Selected project_time: {project_time}")
            bot.send_message(message.chat.id, f"Дата выбрана: {project_time}")


    def project_name(self,message):
        from bot import bot
        bot.send_message(message.chat.id, "Напишите названия проекта ")




            # sql.execute('''INSERT INTO projects (project) VALUES (?)''', (project_bd[num],))

    def close_db():
        db.commit()
        db.close()









