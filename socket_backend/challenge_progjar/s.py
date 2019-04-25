import socket
import pickle
from copy import deepcopy

board = {
        '1,1': 'A1', '1,2': 'A2', '1,3': 'A3',
        '2,1': '--', '2,2': '--', '2,3': '--',
        '3,1': 'B1', '3,2': 'B2', '3,3': 'B3'
}


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('localhost', 9000))
sock.listen()

winposition = {'A' : [['1,1', '2.1', '3.1'], ['1,2', '2,2', '3,2'], ['1,3', '2,3', '3,3'],
           ['2,1', '2,2', '2,3'], ['3,1', '3,2', '3,3'],
           ['1,1', '2,2', '3,3'], ['1,3', '2,2', '3,1']],
               'B' : [['1,1', '2.1', '3.1'], ['1,2', '2,2', '3,2'], ['1,3', '2,3', '3,3'],
           ['2,1', '2,2', '2,3'], ['1,1', '1,2', '1,3'],
           ['1,1', '2,2', '3,3'], ['1,3', '2,2', '3,1']]
            }

def checkwinpos(board, winpos, piece):
    list_coor = []
    for (pos, val) in board.items():
        if val[0] == piece:
            list_coor.append(pos)

    list_coor.sort()
    if list_coor in winposition[piece]:
        return True
    return False


try:
    print("Waiting for p1...")
    p1, addr1 = sock.accept()
    p1.send(b'1')
    print("P1 found. Waiting for p2...")
    p2, addr2 = sock.accept()
    p2.send(b'2')
    print("P2 found")

    while True:

        # p1
        print("Sending board to p1...")
        board_pickled = pickle.dumps(board)
        p1.send(board_pickled)
        print("Waiting for p1 move...")
        data_board = p1.recv(1024)
        print("Received from p1...")
        temp_board = pickle.loads(data_board)
        board = deepcopy(temp_board)

        # check board status here
        iswina = checkwinpos(board, winposition, 'A')
        if iswina:
            print("win")
            p1.send(b'WIN. END.')
            p2.send(b'LOSE. END.')
            break

        # p2
        print("Sending board to p2...")
        board_pickled = pickle.dumps(board)
        p2.send(board_pickled)
        print("Waiting for p2 move...")
        data_board = p2.recv(1024)
        print("Received from p1...")
        temp_board = pickle.loads(data_board)
        board = deepcopy(temp_board)

        # check board status here
        iswinb = checkwinpos(board, winposition, 'B')
        if iswinb:
            print("win2")
            p1.send(b'LOSE. END.')
            p2.send(b'WIN. END.')
            break

except KeyboardInterrupt:
    pass

sock.close()
