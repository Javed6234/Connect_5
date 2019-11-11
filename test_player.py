import unittest
from socket import *

from player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.player = Player(1, "o", self.socket)
    
    def test_get_id(self):
        self.assertIsInstance(self.player.get_id(), int)

    def test_get_disc(self):
        self.assertIsInstance(self.player.get_disc(), str)

    def test_get_connection(self):
        self.assertIsInstance(self.player.get_connection(), socket)
        self.socket.close()

    def tearDown(self):
        self.socket.close()
        
if __name__ == '__main__':
    unittest.main()

