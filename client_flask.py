import requests
from socket import *
import time

def ask_to_join_game(name):
    return requests.post("http://localhost:5000/", json={'username': name})

def check_turn(name, game_id):
    payload = {'username': name, 'game_id': game_id}
    return requests.get("http://localhost:5000/check_turn", params=payload)

def make_move(name, game_id, input):
    data = {'username': name, 'game_id': game_id, 'input': input}
    return requests.put("http://localhost:5000/play", json=data)

def print_board(new_board):
    print(' '.join(str(x) for x in range(1, len(new_board[0])+1)))
    print("\n".join(" ".join(row) for row in new_board))

if __name__ == "__main__":
    res = False
    username = input("Please type in your name: ")
    while res is not True:
        response = ask_to_join_game(username)
        res = response.json()['response']
        print("Found Opponent: %s" % (res))
        time.sleep(5)
    game_id = response.json()['game_id']
    board = response.json()['board']
    game_over = False
    while not game_over:
        is_turn = check_turn(username, game_id)
        if 'board' in is_turn.json():
            board = is_turn.json()['board']
            print(print_board(board))
        if 'win' in is_turn.json():
            if is_turn.json()['win'] == username:
                print("You Won!!!!!")
            else:
                print("You Lost!!!!!")
            break
        if is_turn.json()['turn']:
            user_input = int(input('It’s your turn %s, please enter column (1-9):' % (username)))
            response = make_move(username, game_id, user_input)
            board = response.json()['board']
            print_board(board)
        time.sleep(2)
