import unittest
import pytest
import server_flask
import requests
import json
import flask
from unittest.mock import patch, Mock
from board import Board


class TestServerFlask(unittest.TestCase):
    def setUp(self):
        server_flask.app.config['TESTING'] = True
        server_flask.app.config['WTF_CSRF_ENABLED'] = False

        self.games = {}
        self.players = {}

        self.client = server_flask.app.test_client()
        self.base_url = "http://localhost:5000"
        self.board = Board()

        self.game_id = '4t3rgefbdgrgq4gwer'
        player_one_name = 'player_1'
        player_two_name = 'player_2'
        local_url = 'http://localhost:5000/'

        self.player_one = {
            'username': player_one_name,
            'client_addr': local_url,
            'client_port': 50000,
            'in_game': False,
            'game_id': self.game_id,
            'player_disc': 'x'
        }

        self.player_two = {
            'username': player_two_name,
            'client_addr': local_url,
            'client_port': 50001,
            'in_game': False,
            'game_id': self.game_id,
            'player_disc': 'o'
        }

        game = {
            'game_id': self.game_id,
            'players': (self.player_one, self.player_two),
            'board': self.board,
            'turn': 0,
            'winner': None
        }

        self.games[self.game_id] = game
        self.players[player_one_name] = self.player_one
        self.players[player_two_name] = self.player_two

    def test_index_01(self):
        url = self.base_url + '/'

        player1 = self.client.post(url, environ_base={'REMOTE_ADDR': 'foo', 'REMOTE_PORT': 50000},
                              json={'username': 'test_username'})
        assert player1.status_code == 200
        assert player1.json['response'] == False

        player2 = self.client.post(url, environ_base={'REMOTE_ADDR': 'foo', 'REMOTE_PORT': 50001},
                              json={'username': 'test_username2'})
        assert player2.status_code == 200
        assert player2.json['response'] == True
        assert type(player2.json['game_id']) is str
        assert type(player2.json['board']) is list

    def test_check_turn_02(self):
        with server_flask.app.test_request_context('/check_turn?username=test_username&game_id=4t3rgefbdgrgq4gwer'):
            assert flask.request.path == '/check_turn'
            assert flask.request.args['username'] == 'test_username'
            assert flask.request.args['game_id'] == '4t3rgefbdgrgq4gwer'

    def test_play_03(self):
        url = self.base_url + '/play'
        response = self.client.put(url, environ_base={'REMOTE_ADDR': 'foo', 'REMOTE_PORT': 50000},
                              json={'username': 'test_username', 'game_id': '4t3rgefbdgrgq4gwer', 'input': 5})

        assert response.status_code == 404
        assert response.json['error'] == 'game_id does not exist!'

    def test_is_player_available_04(self):
        server_flask.is_player_available = Mock()

        server_flask.is_player_available.return_value = False, None
        assert server_flask.is_player_available("aaaa") == (False, None)

        server_flask.is_player_available.return_value = True, self.player_one
        assert server_flask.is_player_available("aaaa") == (True, self.player_one)

    def test_create_game_05(self):
        server_flask.create_game = Mock()

        expected_value = {'response': True,
                          'game_id': self.game_id,
                          'board': self.board.board}
        server_flask.create_game.return_value = expected_value
        assert server_flask.create_game(self.player_one, self.player_two) == expected_value

        with patch('server_flask.players', self.players):
            assert server_flask.players == self.players

if __name__ == '__main__':
    unittest.main()
