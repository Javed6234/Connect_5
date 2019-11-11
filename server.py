from socket import *
import pickle
from player import Player
from board import Board

import sys

CONNECTIONS_ALLOWED = 2

MOVE = "move"
GAME_STARTING_ENCODED = "game starting".encode()
WAITING_ENCODED = "waiting for second player".encode()

STAR = "*"
DISC_X = "x"
DISC_O = "o"

CONNECTION_LOSS_WIN = "connection loss"

class Server:
    
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
        self.players = []
        self.turn = 0
        self.board = Board()

    def start_listening(self):
        print('*** Server is starting up on %s port %s ***' % self.server_address)
        try:
            self.sock.bind(self.server_address)
            self.sock.listen(CONNECTIONS_ALLOWED)
        except ConnectionResetError:
            print(error)
            exit(1)

    def get_player(self, index):
        return self.players[index]

    def get_current_player(self):
        return self.players[self.get_turn()]

    def add_player(self, player):
        self.players += [player]

    def set_turn(self):
        self.turn = 1 - self.turn

    def get_turn(self):
        return self.turn

    def setup(self):
        while True:
            try:
                connection, address = self.sock.accept()
                print(address)
                if len(self.players) == 0:
                    player_one = Player(1, DISC_O, connection)
                    self.add_player(player_one)
                    connection.sendall(WAITING_ENCODED)
                elif len(self.players) == 1:
                    player_two = Player(2, DISC_X, connection)
                    self.add_player(player_two)
                    break
            except ConnectionResetError:
                print("Error setting up game")
                exit(1)

        for index in range(len(self.players)):
            player = self.get_player(index)
            try:
                player.connection.sendall(GAME_STARTING_ENCODED)
            except ConnectionResetError:
                print("Error sending data to clients")
                exit(1)

    def win_message(self, reason=None):
        message = {"win": None}
        pickled_win = pickle.dumps(message)
        message = {"lose": None}
        pickled_lose = pickle.dumps(message)
        # If the reason is a disconnect win
        if reason == CONNECTION_LOSS_WIN:
            for index in range(len(self.players)):
                player = self.get_player(index)
                try:
                    player.connection.send(pickled_win)
                except ConnectionResetError:
                    print("Error sending data to clients due to connection loss")
        else:
            try:
                winner = self.get_current_player()
                winner.get_connection().send(pickled_win)
                self.set_turn()
                loser = self.get_current_player()
                loser.get_connection().send(pickled_lose)
            except ConnectionResetError:
                print("Error sending data to clients")

    def close_client_connections(self):
        for index in range(len(self.players)):
            player = self.get_player(index)
            player.connection.close()

    def start_game(self):
        while True:
            player = self.get_current_player()
            conn = player.get_connection()

            # Tell player it's their turn
            message = {MOVE: self.board.board}
            pickled_message = pickle.dumps(message)
            try:
                conn.send(pickled_message)
            except ConnectionResetError:
                print("Error sending data to clients")
                self.win_message(CONNECTION_LOSS_WIN)
                break

            # Receive input column from player
            try:
                input_column = conn.recv(1024)
            except ConnectionResetError:
                print("Error receiving data from clients")
                self.win_message(CONNECTION_LOSS_WIN)
                break
            if not input_column:
                self.win_message(CONNECTION_LOSS_WIN)
                break
            input_column = int(input_column.decode())
            
            print("Player", self.turn)
            print("input_column", input_column)
            if self.board.add_disc(input_column, player):
                # Check if any player has won
                if self.board.check_win():
                    # Send winning message
                    self.win_message()
                    break
                self.set_turn()
        # Close connetion to clients
        self.close_client_connections()
        

    def run(self):
        self.start_listening()
        self.setup()
        self.start_game()
        

if __name__ == '__main__':
    s = Server()
    s.run()

                    
            
        
