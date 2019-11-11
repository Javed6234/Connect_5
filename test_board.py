import unittest
from socket import *

from board import *

class FakePlayer:
    def get_disc(self):
        return 'o'

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player = FakePlayer()

    def test_01_default_board(self):
        test_board = [['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                      ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                      ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                      ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                      ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                      ['*', '*', '*', '*', '*', '*', '*', '*', '*']]
        self.assertTrue(self.board.board == test_board)

    def test_add_disc(self):
        # Add disc in column 3
        test_add_board = [['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', 'o', '*', '*', '*', '*', '*', '*']]
        
        self.board.add_disc(3, self.player)
        self.assertTrue(self.board.board == test_add_board)

    def test_check_horizontal_win(self):
        test_win_board = [['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', 'o', 'o', 'o', 'o', 'o'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*']]
        self.board.board = test_win_board
        self.assertTrue(self.board.check_horizontal_win())

    def test_fail_check_horizontal_win(self):
        test_win_board = [['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', 'o', 'o', 'o', 'o', 'x']]
        self.board.board = test_win_board
        self.assertFalse(self.board.check_horizontal_win())

    def test_check_vertical_win(self):
        test_win_board = [['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', 'o'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', 'o'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', 'o'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', 'o'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', 'o']]
        self.board.board = test_win_board
        self.assertTrue(self.board.check_vertical_win())
        
    def test_fail_check_vertical_win(self):
        test_win_board = [['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', 'o'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', 'x'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', 'o'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', 'o'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', 'o']]
        self.board.board = test_win_board
        self.assertFalse(self.board.check_vertical_win())
        
    def test_check_positive_diag_win(self):
        test_win_board = [['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', 'o', '*', '*'],
                          ['*', '*', '*', '*', '*', 'o', 'x', '*', '*'],
                          ['*', '*', '*', '*', 'o', '*', 'x', '*', '*'],
                          ['*', '*', '*', 'o', '*', '*', 'x', '*', '*'],
                          ['*', '*', 'o', '*', '*', '*', 'x', '*', '*']]
        self.board.board = test_win_board
        self.assertTrue(self.board.check_positive_diag_win())

    def test_fail_check_positive_diag_win(self):
        test_win_board = [['*', '*', '*', '*', '*', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', 'o', '*', '*'],
                          ['*', '*', '*', '*', '*', 'x', 'x', '*', '*'],
                          ['*', '*', '*', '*', 'o', '*', 'x', '*', '*'],
                          ['*', '*', '*', 'o', '*', '*', 'x', '*', '*'],
                          ['*', '*', 'o', '*', '*', '*', 'x', '*', '*']]
        self.board.board = test_win_board
        self.assertFalse(self.board.check_positive_diag_win())

    def test_check_negative_diag_win(self):
        test_win_board = [['*', '*', '*', '*', 'o', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', 'o', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', 'o', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', 'o', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', 'o'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*']]
        self.board.board = test_win_board
        self.assertTrue(self.board.check_negative_diag_win())

    def test_fail_check_negative_diag_win(self):
        test_win_board = [['*', '*', '*', '*', 'o', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', 'x', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', 'o', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', 'o', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', 'o'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*']]
        self.board.board = test_win_board
        self.assertFalse(self.board.check_negative_diag_win())

    def test_check_win(self):
        test_win_board = [['*', '*', '*', '*', 'o', '*', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', 'o', '*', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', 'o', '*', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', 'o', '*'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', 'o'],
                          ['*', '*', '*', '*', '*', '*', '*', '*', '*']]
        self.board.board = test_win_board
        self.assertTrue(self.board.check_win())
        
        
        
if __name__ == '__main__':
    unittest.main()

