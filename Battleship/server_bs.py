import socket
import threading
import sqlite3
import pickle

import dbconn
from player import Player

class ClientThread(threading.Thread):
    def __init__(self, sock: socket, address: tuple, player_list: dict):
        threading.Thread.__init__(self)
        self.sock = sock
        self.address = address
        self.live = True
        self.player_list = player_list

        # describes player in thread
        self.player = Player("")


    def run(self):
        print("Sending HELO to", self.address)
        self.sock.send(b"HELO")
        self.conn = sqlite3.connect("battleship.db")
        while self.live:

            data = self.sock.recv(1024)
            data_splitted = data.decode().split()
            command, argument = data_splitted[0], " ".join(data_splitted[1:])
            if command == "LUSR":
                print(self.login(argument))
            if command == "RUSR":
                print(self.register(argument))
            if command == "PLST":
                print(self.showPlayerList())
            if command == "QUIT":
                print(self.address, "said goodbye :(")
                self.sock.send(b"BYE")
                self.sock.close()
                self.live = False

                # if already logged in, delete from session
                if self.player.name:
                    self.player_list.pop(self.player.name)

                self.conn.close()


    def login(self, user):
        detail = dbconn.get_user(self.conn, user)
        if not detail:
            self.sock.send(b"401 User Name Null")
            return "401"

        user, password = detail

        # check for double login
        if user in self.player_list:
            self.sock.send(b"404 User Already Logged In")
            return "402"
        self.sock.send(b"201 Proceed Password Login")
        data = self.sock.recv(1024)
        data_splitted = data.decode().split()
        command, argument = data_splitted[0], " ".join(data_splitted[1:])
        if command == "LPAS":
            if argument != password:
                self.sock.send(b"402 Password Not Recognized")
                return "402"

            # successful login
            self.player.name = user
            self.player.loggedin = True

            # add current player to player_list
            self.player_list[user] = self.player

            self.sock.send(b"290 Login OK")
            return "290"
        else:
            self.sock.send(b"499 Unknown Command")
            return "499"


    def register(self, user):
        detail = dbconn.get_user(self.conn, user)
        if detail:
            self.sock.send(b"403 User Name Already Registered")
            return "403"

        self.sock.send(b"202 Proceed Password Register")
        data = self.sock.recv(1024)
        data_splitted = data.decode().split()
        command, argument = data_splitted[0], " ".join(data_splitted[1:])
        if command == "RPAS":
            detail = dbconn.register(self.conn, user, argument)

            self.sock.send(b"291 Register OK")
            return "410"
        else:
            self.sock.send(b"499 Unknown Command")
            return "499"

    def showPlayerList(self):
        plist = []
        for name, player in self.player_list.items():
            plist += [player]
            print(player.name)
        # pickled_list =
        self.sock.send(b"VIEW PLAYER LIST")
        return "204"


class BattleshipServer:
    def __init__(self, ip = "127.0.0.1", port = 9000):

        # prepping up socket
        self.servsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.servsock.bind((ip, port))
        self.servsock.listen()

        self.player_list = {}
        self.servwaiting = threading.Thread(target=self.waitForPlayer)
        self.servwaiting.start()

    def waitForPlayer(self):
        print("Battleship Server is up. Waiting for player...")
        while True:
            conn, addr = self.servsock.accept()
            print("New connection initiated", addr)
            client = ClientThread(conn, addr, self.player_list)
            client.start()

bsserver = BattleshipServer()

# try:
#     while True:
#         client_sock, addr = server_sock.accept()
#         client_thread = ClientThread(client_sock, addr)
#         client_thread.start()
# except KeyboardInterrupt:
#     pass

# server_sock.close()