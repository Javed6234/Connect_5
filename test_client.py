import unittest
from unittest.mock import patch, call
from client import Client
from server import Server

from socket import *

class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.client = Client()

    @patch('builtins.input', side_effect=["Genesys"])
    def test_set_player_name(self, mock_input):
        # Input is "Genesys" but returns None
        self.assertIsNone(self.client.set_player_name())
        
    def test_fail_connect_to_server(self):
        failed_expected = "Could not connect to Server!"
        connection_status = self.client.connect_to_server()
        self.assertEqual(connection_status, failed_expected)

    def test_fail_wait_for_server(self):
        failed_expected = "Connection has been lost to the server"
        server_status = self.client.wait_for_server()
        self.assertEqual(server_status, failed_expected)
        
    def test_connection_type(self):
        self.assertIsInstance(self.client.sock, socket)
        
    @classmethod
    def tearDownClass(self):
        self.client.sock.close()
        
if __name__ == '__main__':
    unittest.main()
