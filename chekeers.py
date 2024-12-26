import random , string

letters = [chr(i) for i in range(96,105)]

def start_game():
    global users
    print()
    players[users[0],users[0]+5] =  ("⬛", "⬜") if random.randint(0,1) else ("⬜", "⬛")
    for row in range(8):
        btn = []
        for col, col_letters in enumerate(letters):
            if (col+row) %2==0:
                if row <3:
                    btn.append("⬛")
                elif row >4:
                    btn.append("⬜")
                else:
                    btn.append("  ")
            else:
                btn.append(" ")

        print(btn)


users=[] # создает масив с юзерами
players = {}
while True:
    user_sleep= random.randint(0,3) # создания  id юзера
    if len(users) != 2: #проверка количество юзеров
        users.append(user_sleep) #добавляет id юзеров
    else:
        break
start_game()
