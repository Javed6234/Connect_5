import unittest
from client import Client
from server import Server

from socket import *

WAITING = "waiting for second player"

class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.server = Server()
        self.server.run()
        self.client = Client()

    def test_connection_type(self):
        self.assertIsInstance(self.client.sock, socket)
        self.assertIsInstance(self.server.sock, socket)

    def test_wait_for_server(self):
        self.client.wait_for_server()
        
    @classmethod
    def tearDownClass(self):
        self.client.sock.close()
        self.server.sock.close()
        
if __name__ == '__main__':
    unittest.main()

