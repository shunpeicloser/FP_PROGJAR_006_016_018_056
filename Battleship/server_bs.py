import socket
import threading
import sqlite3
import pickle

import dbconn
from player import Player

class ClientThread(threading.Thread):
    def __init__(self, sock: socket, address: tuple, player_list: dict, socket_list: dict):
        threading.Thread.__init__(self)
        self.sock = sock
        self.address = address
        self.live = True
        self.player_list = player_list
        self.socket_list = socket_list

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
            if command == "INVT":
                print(self.invite(argument))
            if command == "QUIT":
                name = self.player.name
                print(name, self.address, "said goodbye :(")

                self.sock.send(b"BYE")
                self.sock.close()
                self.live = False

                # if already logged in, delete from session
                if self.player.name:
                    for sock_name, sock in self.socket_list[self.player.name].items():
                        print("closing", sock_name, "socket of", self.player.name)
                        sock.close()
                    self.player_list.pop(self.player.name)

                # self.conn.close()


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
            # self.player.sock = self.sock
            self.socket_list[user] = {}
            self.socket_list[user]["main"] = self.sock

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
            if name == self.player.name or player.is_ingame():
                continue
            plist += [player]
            print(player.name)
        pickled_list = pickle.dumps(plist)
        self.sock.send(pickled_list)
        return "204"

    def invite(self, opponent):
        if self.player_list[opponent].is_ingame():
            print(opponent, "is currently in game, couldn't send challenge")
            self.sock.send("405 Player is In Game")
            return "405"

        print(self.player.name, "is challenging", opponent)
        self.socket_list[opponent]["challenge"].send("INVD {}".format(self.player.name).encode())
        # self.sock.send(b"293 Challenge Sent")

        # wait for opponent response
        # resp = self.socket_list[opponent]["main"].recv(1024).decode()
        # print(opponent, resp)
        # if resp == "OK":
        self.socket_list[opponent]["challenge"].send(b"293 Battle Start")
        self.sock.send(b"293 Battle Start")

        # set status for both players
        self.player.goPlay()
        self.player_list[opponent].goPlay()

        return "293"

class BattleshipServer:
    def __init__(self, ip = "127.0.0.1", port = 9000):

        # prepping up socket
        self.servsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.servsock.bind((ip, port))
        self.servsock.listen()

        # prepping up challenge socket
        self.challenge_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.challenge_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.challenge_sock.bind((ip, port+1))
        self.challenge_sock.listen()

        self.player_list = {}
        self.socket_list = {} # name -> {main_socket, challenge_socket}
        self.servwaiting = threading.Thread(target=self.waitForPlayer)
        self.csockwaiting = threading.Thread(target=self.pairChallengeSocket)
        self.servwaiting.start()
        self.csockwaiting.start()

    def waitForPlayer(self):
        print("Battleship Server is up. Waiting for player...")
        while True:
            conn, addr = self.servsock.accept()
            print("New connection initiated", addr)
            client = ClientThread(conn, addr, self.player_list, self.socket_list)
            client.start()

    def pairChallengeSocket(self):
        while True:
            conn, addr = self.challenge_sock.accept()
            command, name = conn.recv(1024).decode().split()
            if command == "CSCK":
                if name in self.player_list:
                    print("Challenge sock with", name, "initiated")
                    self.socket_list[name]["challenge"] = conn
                    self.socket_list[name]["challenge"].send(b"PAIRED")

bsserver = BattleshipServer()

# try:
#     while True:
#         client_sock, addr = server_sock.accept()
#         client_thread = ClientThread(client_sock, addr)
#         client_thread.start()
# except KeyboardInterrupt:
#     pass

# server_sock.close()