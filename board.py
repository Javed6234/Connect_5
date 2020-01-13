from player import Player

ROWS = 6
COLUMNS = 9
NUM_TO_CONNECT = 3
STAR = "*"


class Board:
    def __init__(self):
        self.board = [[STAR for i in range(COLUMNS)] for j in range(ROWS)]
        
    def add_disc(self, col, player_disc):
        # Search up the column from (ROWS - 1) to 0
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col - 1] == STAR:
               self.board[row][col - 1] = player_disc
               print(self)
               return True
        return False

    def check_vertical_win(self):
        # Check vertical win
        player_disc = self.board[0][0]
        for col in range(COLUMNS):
            counter = 0
            for row in range(ROWS):
                disc = self.board[row][col]
                if disc != STAR:
                    if disc == player_disc:
                        counter += 1
                    else:
                        player_disc = disc
                        counter = 1
                    if counter == NUM_TO_CONNECT:
                        return True

    def check_horizontal_win(self):
        # Check horizontal win
        player_disc = self.board[0][0]
        for row in range(ROWS):
            counter = 0
            for col in range(COLUMNS):
                disc = self.board[row][col]
                if disc != STAR:
                    if disc == player_disc:
                        counter += 1
                    else:
                        player_disc = disc
                        counter = 1
                    if counter == NUM_TO_CONNECT:
                        return True
                    
    def check_positive_diag_win(self):
        # Check positive diagonal win
        player_disc = self.board[0][0]
        for row in range((NUM_TO_CONNECT - 1), ROWS):
            counter = 0
            for col in range(row + 1):
                disc = self.board[row-col][col]
                if disc != STAR:
                    if disc == player_disc:
                        counter += 1
                    else:
                        player_disc = disc
                        counter = 1
                    if counter == NUM_TO_CONNECT:
                        return True

        player_disc = self.board[0][0]
        for col in range(1, COLUMNS - (NUM_TO_CONNECT - 1)):
            counter = 0
            for row in range(ROWS):
                if row+col < COLUMNS:
                    disc = self.board[(ROWS - 1) - row][row+col]
                    if disc != STAR:
                        if disc == player_disc:
                            counter += 1
                        else:
                            player_disc = disc
                            counter = 1
                        if counter == NUM_TO_CONNECT:
                            return True

    def check_negative_diag_win(self):
        # Check negative diagonal win
        player_disc = self.board[0][0]
        for row in range(ROWS - (NUM_TO_CONNECT - 1)):
            counter = 0
            for col in range(ROWS - row):
                disc = self.board[row+col][col]
                if disc != STAR:
                    if disc == player_disc:
                        counter += 1
                    else:
                        player_disc = disc
                        counter = 1
                    if counter == NUM_TO_CONNECT:
                        return True
        
        player_disc = self.board[0][0]
        for col in range(1, COLUMNS - (NUM_TO_CONNECT - 1)):
            counter = 0
            for row in range(ROWS):
                if row+col < COLUMNS:
                    disc = self.board[row][row+col]
                    if disc != STAR:
                        if disc == player_disc:
                            counter += 1
                        else:
                            player_disc = disc
                            counter = 1
                        if counter == NUM_TO_CONNECT:
                            return True

    def check_win(self):
        return self.check_vertical_win() or \
        self.check_horizontal_win() or \
        self.check_positive_diag_win() or \
        self.check_negative_diag_win()


    def __str__(self):
        print(' '.join(str(x) for x in range(1, COLUMNS + 1)))
        return "\n".join(" ".join(row) for row in self.board)
