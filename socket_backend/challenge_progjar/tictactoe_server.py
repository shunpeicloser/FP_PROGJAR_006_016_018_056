import pickle
import threading
from copy import deepcopy

class TicTacToe(threading.Thread):
    def __init__(self, playerA, playerB):
        self.board = {
                '1,1': 'A1', '1,2': 'A2', '1,3': 'A3',
                '2,1': '--', '2,2': '--', '2,3': '--',
                '3,1': 'B1', '3,2': 'B2', '3,3': 'B3'
        }
        self.winposition = {'A' : [
                                ['1,1', '2.1', '3.1'], ['1,2', '2,2', '3,2'], ['1,3', '2,3', '3,3'], # vertical
                                ['2,1', '2,2', '2,3'], ['3,1', '3,2', '3,3'], # horizontal
                                ['1,1', '2,2', '3,3'], ['1,3', '2,2', '3,1'] # diagonal
                            ],
                            'B' : [
                                ['1,1', '2.1', '3.1'], ['1,2', '2,2', '3,2'], ['1,3', '2,3', '3,3'], # vertical
                                ['2,1', '2,2', '2,3'], ['1,1', '1,2', '1,3'], # horizontal
                                ['1,1', '2,2', '3,3'], ['1,3', '2,2', '3,1'] # diagonal
                            ]
        }
        self.playerA = playerA
        self.playerB = playerB

    def checkwinpos(self, board, winpos, piece):
        list_coor = []
        for (pos, val) in board.items():
            if val[0] == piece:
                list_coor.append(pos)

        list_coor.sort()
        if list_coor in self.winposition[piece]:
            return True
        return False


    def run(self):
        while True:
            # p1
            print("Sending board to p1...")
            board_pickled = pickle.dumps(board)
            self.playerA.conn.send(board_pickled)
            print("Waiting for p1 move...")
            data_board = self.playerA.conn.recv(1024)
            print("Received from p1...")
            temp_board = pickle.loads(data_board)
            board = deepcopy(temp_board)

            # check board status here
            iswina = self.checkwinpos(board, self.winposition, 'A')
            if iswina:
                print("win")
                self.playerA.conn.send(b'WIN. END.')
                self.playerB.conn.send(b'LOSE. END.')
                break

            # p2
            print("Sending board to p2...")
            board_pickled = pickle.dumps(board)
            self.playerB.conn.send(board_pickled)
            print("Waiting for p2 move...")
            data_board = self.playerB.conn.recv(1024)
            print("Received from p1...")
            temp_board = pickle.loads(data_board)
            board = deepcopy(temp_board)

            # check board status here
            iswinb = self.checkwinpos(board, self.winposition, 'B')
            if iswinb:
                print("win2")
                self.playerA.conn.send(b'LOSE. END.')
                self.playerB.conn.send(b'WIN. END.')
                break
