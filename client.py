from socket import *
import pickle

import sys

MOVE = "move"
GAME_STARTING = "game starting"
WAITING = "waiting for second player"
WIN = "win"
LOSE = "lose"

class Client:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.host = gethostbyname(gethostname())
        if len(sys.argv) > 1:
            self.host = sys.argv[1]
            if self.host == "''":    
                self.host = gethostbyname(gethostname())
        self.port = 10001
        if len(sys.argv) > 2:
            self.port = int(sys.argv[2])
        self.server_address = (self.host, self.port)
        self.name = input("Please type in your name: ")
        try:
            self.sock.connect(self.server_address)
        except ConnectionRefusedError:
            print("Could not connect to Server!")
            exit(0)
        print("Connected to Server!")

    def wait_for_server(self):
        while True:
            try:
                data = self.sock.recv(1024).decode()
            except ConnectionResetError:
                print()
                print("Connection has been lost to the server")
                exit(0)
            
            if data == WAITING:
                print(WAITING)
            elif data == GAME_STARTING:
                break

    def win_message(self):
        print("******************")
        print("You win %s!!!!!!!!!!!" % (self.name))
        print("******************")

    def lose_message(self):
        print("******************")
        print("You lose %s!!!!!!!!!!!" % (self.name))
        print("******************")
        
    def run(self):
        while True:
            try:
                data = pickle.loads(self.sock.recv(4096))
            except ConnectionResetError:
                print()
                print("Connection has been lost to the server")
                break
            if MOVE in data:
                updated_board = data[MOVE]
                print(' '.join(str(x) for x in range(1, len(updated_board[0])+1)))
                print("\n".join(" ".join(row) for row in updated_board))
                # Ask for valid column input
                valid_input = False
                while not valid_input:
                    user_input = input('It’s your turn %s, please enter column (1-9):' % (self.name))
                    try:
                       col = int(user_input)
                    except ValueError:
                        print("Please provide an integer!")
                        continue
                    if col in range(1, 10):
                        valid_input = True
                    else:
                        print("Please provide a number between 1-9")
                self.sock.sendall(user_input.encode())

            if WIN in data:
                self.win_message()
                break

            if LOSE in data:
                self.lose_message()
                break
        self.sock.close()




c = Client()
c.wait_for_server()
c.run()
