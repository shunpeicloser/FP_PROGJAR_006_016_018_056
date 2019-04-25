import socket
import threading

class Player:
    def __init__(self, name: str, conn: socket):
        self.name = name
        self.conn = conn

class Game:
    def __init__(self, host = '10.151.34.154', port = 9000):
        # create server socket
        self.address = (host, port)
        self.servsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servsock.bind(self.address)
        self.servsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.servsock.listen()

        self.player_list = {}
        self.gate = threading.Thread(target=self.waitForPlayer)
        self.gate.start()


    def waitForPlayer(self):
        print("Game created waiting for player...")
        while True:
            conn, addr = self.servsock.accept()
            print("New player!")
            threading.Thread(target=self.playerThread, args=(conn, addr)).start()

    def playerThread(self, conn: socket, addr: tuple):
        player_name = conn.recv(1024).decode()
        print("Welcome,", player_name)
        player_object = Player(player_name, conn)
        self.player_list[player_name] = player_object
        while True:
            command = conn.recv(1024).decode().split()
            print(command)
            if command[0] == "quit":
                conn.send(b'well recvd')
                self.player_list.pop(player_name, None)
                conn.close()
                print(player_name, 'is quiting')
                break
            elif command[0] == 'list':
                conn.send(self.listPlayer().encode())
            elif command[0] == 'send':
                to = command[1]
                player = self.player_list[to]
                player.conn.send(' '.join(command[2:]).encode())
                conn.send(b'well recvd. msg sent')
            else:
                conn.send(b'well recvd')

    def listPlayer(self) -> str:
        tosend = " == List Player =="
        for name in self.player_list:
            tosend += '\n' + name
        return tosend


a = Game()