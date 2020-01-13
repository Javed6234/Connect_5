from flask import Flask, redirect, url_for, request, render_template, session, jsonify
from uuid import uuid4
from board import Board

app = Flask(__name__)
app.secret_key = b'Yx0t\xb2\xc9@FT\x18\xb9K%\xf9m\x1a'

players = {}
games = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.json['username']
        client_addr = request.environ['REMOTE_ADDR']
        client_port = request.environ['REMOTE_PORT']

        player = {
            'username': name,
            'client_addr': client_addr,
            'client_port': client_port,
            'in_game': False,
            'game_id': None,
            'player_disc': None
        }

        global players
        if name not in players:
            players[name] = player
        else:
            if players[name]['in_game']:
                game_id = players[name]['game_id']
                board = games[game_id]['board']
                return jsonify(response=True, game_id=game_id, board=board.board)

        player_is_available, other_player = is_player_available(player)
        # There is not an existing matching opponent, so create a game
        if player_is_available:
            # There is a matching opponent, so join that game session
            return create_game(player, other_player)
        return jsonify(response=False)
    return ""

def is_player_available(current_player):
    for username in players:
        if current_player['username'] != username and not players[username]['in_game']:
            return True, players[username]
    return False, None

def create_game(player, other_player):
    board = Board()
    player['in_game'] = True
    other_player['in_game'] = True
    game_id = str(uuid4())
    player['game_id'] = game_id
    other_player['game_id'] = game_id
    player['player_disc'] = 'x'
    other_player['player_disc'] = 'o'

    game = {
        'game_id': game_id,
        'players': (player, other_player),
        'board': board,
        'turn': 0,
        'winner': None
    }

    games[game_id] = game
    return jsonify(response=True, game_id=game_id, board=board.board)

@app.route('/check_turn', methods=['GET'])
def check_turn():
    name = request.args.get('username')
    game_id = request.args.get('game_id')
    game = games[game_id]
    board = game['board']

    if game['winner']:
        return jsonify(win=game['winner'])

    turn_index = game['turn']
    player = game['players'][turn_index]
    if player['username'] != name:
        return jsonify(turn=False)
    return jsonify(turn=True, board=board.board)

@app.route('/play', methods=['PUT'])
def play():
    name = request.json['username']
    game_id = request.json['game_id']
    input = request.json['input']
    game = games[game_id]
    board = game['board']

    turn_index = game['turn']
    player = game['players'][turn_index]

    if board.add_disc(int(input), player['player_disc']):
        # Check if any player has won
        if board.check_win():
            game['winner'] = name

    game['turn'] = 1 - game['turn']
    return jsonify(board=board.board)