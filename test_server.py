import unittest
from socket import *

from server import Server
from player import Player

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.server = Server()
        self.player_socket = socket(AF_INET, SOCK_STREAM)
        self.test_player = Player(1, "o", self.player_socket)

    def test_01_default_players(self):
        self.assertTrue(len(self.server.players) == 0)

    def test_02_default_turn(self):
        self.assertTrue(self.server.turn == 0)
        
    def test_03_add_player(self):
        self.server.add_player(self.test_player)
        self.assertTrue(len(self.server.players) == 1)

    def test_04_get_player(self):
        self.assertTrue(self.test_player.get_id() == self.server.get_player(0).get_id())

    def test_05_get_current_player(self):
        self.assertTrue(self.test_player.get_id() == self.server.get_current_player().get_id())

    def test_06_set_turn(self):
        self.server.set_turn()
        self.assertTrue(self.server.get_turn() == 1)

    @classmethod
    def tearDownClass(self):
        self.player_socket.close()
        
if __name__ == '__main__':
    unittest.main()

