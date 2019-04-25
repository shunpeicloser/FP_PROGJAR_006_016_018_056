import socket
import pickle
from copy import deepcopy

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9000))

# check whoami
p = sock.recv(1024)
p = p.decode()
print("You are player", p, chr(int(p)+64))

def draw(board):
    #b = [['' for i in range(3)] for _ in range(3)]
    row = 1
    col = 1
    while row <= 3:
        print('|', end = '')
        while col <= 3:
            print('{0}|'.format(board[str(row)+','+str(col)]), end = '')
            col += 1
        print()
        row += 1
        col = 1

def move(board, piece, coor):
    # search for piece coor
    tcor = ""
    for (key, val) in board.items():
        if val == piece:
            tcor = key
            break

    if board[coor] != "--":
        return False

    # manhattan
    co_x = int(coor[0])
    co_y = int(coor[2])

    tc_x = int(tcor[0])
    tc_y = int(tcor[2])

    if abs(co_x - tc_x) > 1 or abs(co_y - tc_y) > 1:
        return False

    board[tcor], board[coor] = board[coor], board[tcor]
    return True

while True:
    print("Please wait for your turn to move...")
    data_board = sock.recv(1024)
    if data_board == b'WIN. END.':
        print("YOU WIN CONGRATS")
        break
    if data_board == b'LOSE. END.':
        print("YOU LOSE CONGRATS")
        break
    board = pickle.loads(data_board)
    draw(board)
    while True:
        print("Make your move. Select your piece")
        piece = input()
        print("Select coordinate")
        coor = input()
        if not move(board, piece, coor):
            print("Illegal Move. Retry.")
            continue
        break
    temp_board = deepcopy(board)
    draw(temp_board)
    board_pickled = pickle.dumps(temp_board)
    sock.send(board_pickled)
    print("Waiting for opponent's move...")

sock.close()

