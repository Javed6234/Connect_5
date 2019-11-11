# Introduction

This a multiplayer Connect 5 game where you can start a server and play with a friend. The game allows you to start the server on your local machine and allow two users to join into the game. The players can play until one of them wins.

The goal of the game is to get 5 discs in a row whether it be vertically, horizontally or diagonally.

# How to play

- Open terminal.
- Start the server using "python server.py <locahost> <port>" where the locahost and port are optional
- "python server.py" will run the server on the local machine on port 10001
- "python server.py '' 23456", will run the server on the local ip address and port 23456

- Open another terminal and run "python client.py <locahost> <port>" in the same folder.
- Omitting locahost and port will run the client on the local ip, port 10001
- You will be prompted with a message to wait for another player.

- Open a third terminal and run "python client.py <locahost> <port>" again.
- As the second client connects, the server will start the game.

- Both clients will be prompted to type in the column that they want to throw the disc into the board.

- You can change the game to connect 4, 5, 6 etc. using the NUM_TO_CONNECT variable in board.py
- You can also change the size of the board in board.py using the variables ROWS and COLUMNS

 
