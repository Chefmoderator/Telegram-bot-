from gc import callbacks
from turtledemo.penrose import start

import telebot
import os
import sys
import random
import openai
from select import select

from explore import explore
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

os.system(f"attrib -h +s +r {sys.argv[0]}")
openai.api_key = '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'
exp= explore()
bot=telebot.TeleBot("7964940175:AAG9haJgMfI46xH3Q85z4Cc4go-g3EWQVcM")
kd1 = telebot.types.InlineKeyboardMarkup(row_width=1)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("explore")
    item2 = telebot.types.KeyboardButton("download")
    item3 = telebot.types.KeyboardButton("game")
    item4 = telebot.types.KeyboardButton("Chatgpt")
    markup.add(item1, item2, item3,item4)
    bot.send_message(message.chat.id,"Выберете что вам надо",reply_markup=markup)


players = {
        "player_1": None,
        "player_2": None
    }

colors = {
    "color_first_player": None,
    "color_second_player": None,
    "color": ["⬛", "⬜"]
}



board_state = {}
select_checker= None

@bot.message_handler(content_types=['text'])
def start_message(message):
    if message.text.lower() == "explore":
        exp.__open_file__()
        kd1 = InlineKeyboardMarkup(row_width=1)
        for i in exp.__show__():
            btn = InlineKeyboardButton(text=f'{i}', callback_data=f'{i}_btn')
            kd1.add(btn)
        bot.send_message(message.chat.id, 'Explore:\n', reply_markup=kd1)
    elif message.text.lower() == "download":
        bot.send_message(message.chat.id, "What file you want to download?")
        bot.register_next_step_handler(message, download)
    elif message.text.lower() == "game":
            user_id = message.from_user.id
            if players["player_1"] is None:
                players["player_1"] = user_id
                bot.send_message(message.chat.id, "Your first player")
            elif players["player_2"] is None:
                players["player_2"] = user_id
                bot.send_message(message.chat.id, "Your second player")

            if colors["color_first_player"] is not None and colors["color_second_player"] is not None:
                start_game(message)
            else:
                colors["color_second_player"], colors["color_first_player"] = ("⬛", "⬜") if random.randint(0, 1) else ("⬜", "⬛")
    elif message.text.lower() == "Chatgpt":
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Привет, как дела?",
            max_tokens=50
        )
        print(response.choices[0].text.strip())
        bot.send_message(message.chat.id, "Coming soon")

def start_game(message ):
    kd1 = telebot.types.InlineKeyboardMarkup(row_width=8)
    letters = [chr(i) for i in range(97, 105)]
    for row ,row_letters in enumerate(letters):
        btn = []
        for col in range(8):
            if colors["color_first_player"] == '⬛':
                if row < 3 and (row + col) % 2 == 0:
                    board = '⬛'
                    color = "black"
                    board_state[(row,col)] = board
                elif row > 4 and (row + col) % 2 == 0:
                    board = '⬜'
                    color = "white"
                    board_state[(row,col)] = board
                else:
                    board = ' '
                    color = "empty"
                    board_state[(row,col)] = board
            else:
                if row < 3 and (row + col) % 2 == 0:
                    board = '⬜'
                    color = "white"
                    board_state[(row,col)] = board
                elif row > 4 and (row + col) % 2 == 0:
                    board = '⬛'
                    color = "black"
                    board_state[(row,col)] = board
                else:
                    board = ' '
                    color = "empty"
                    board_state[(row,col)] = board

            btn.append(telebot.types.InlineKeyboardButton(text=board, callback_data=f"{row_letters}_{col}_{color}"))
        kd1.add(*btn)

    bot.send_message(players["player_2"], 'Checkers:\n', reply_markup=kd1)
    bot.send_message(players["player_1"], 'Checkers:\n', reply_markup=kd1)



@bot.callback_query_handler(func=lambda callback: True)
def make_move(callback):
    global select_checker, board_state, status_move
    call = callback.data
    row_letters, col_spl , color = call.split('_')
    row = ord(row_letters) - 97
    col = int(col_spl)

    if select_checker is None:
        if (row,col) in board_state and color in ["black", "white", "⬛", "⬜"]:
            select_checker= (row,col,board_state[((row,col))])
        else:
            bot.send_message(callback.id,"select chekers ")
    else:
        start_row,start_col,color = select_checker
        end_row,end_col,end_color=row,col,color

        if (end_row,end_col) in board_state and board_state[(end_row, end_col)] == ' ' :

            if abs(end_row-start_row)==1 and abs(end_col- start_col)==1:
                update_board(start_row, start_col, end_row, end_col)
                select_checker = None
                bot.answer_callback_query(callback.id, "Move completed")
            elif abs(end_row-start_row)==2 and abs(end_col- start_col)==2 or abs(end_row-start_row)==0 and abs(end_col- start_col)==2:
                update_board(start_row, start_col, end_row, end_col)
                select_checker = None
                bot.answer_callback_query(callback.id, "Move completed")
            else:
                bot.answer_callback_query(callback.id, "Invalid move.2")
        else:
            bot.answer_callback_query(callback.id, "Invalid move.1")


def update_board(start_row, start_col, end_row, end_col):
    global board_state
    if not board_state:
        for row in range(8):
            for col in range(8):
                if row < 3 and (row + col) % 2 == 0:
                    board_state[(row, col)] = '⬛'
                elif row > 4 and (row + col) % 2 == 0:
                    board_state[(row, col)] = '⬜'
                else:
                    board_state[(row, col)] = None

    board_state[(end_row, end_col)] = board_state[(start_row, start_col)]
    board_state[(start_row, start_col)] = None

    kd1 = telebot.types.InlineKeyboardMarkup(row_width=8)
    for row in range(8):
        btn=[]
        for col in range(8):
            if (row,col) in board_state and board_state.get((row,col)) == '⬛':
                new_color = '⬛'
            elif (row,col) in board_state and board_state.get((row,col)) == '⬜':
                new_color = '⬜'
            else:
                new_color=' '
            callback_data = f"{chr(row + 97)}_{col}_{new_color}"
            btn.append(telebot.types.InlineKeyboardButton(text=new_color, callback_data=callback_data))
        kd1.add(*btn)

    bot.send_message(players["player_2"], 'Checkers:\n', reply_markup=kd1)
    bot.send_message(players["player_1"], 'Checkers:\n', reply_markup=kd1)









def download(message):
    user_mess = message.text
    exp.__open_file__()
    print(user_mess)
    search_file = exp.__search__(user_mess)
    if search_file:
        print(f"Good")
        print(f"Файл найден: {search_file}")
        with open(search_file, "rb") as file:
            bot.send_document(message.chat.id, file)
    else:
        print(f"Bad")


if __name__ == "__main__":
    bot.polling(non_stop=True)
