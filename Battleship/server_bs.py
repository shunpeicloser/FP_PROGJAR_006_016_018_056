import socket
import threading
import sqlite3
import pickle

import dbconn
from player import Player

class BattleSession(threading.Thread):
    def __init__(self, session_id, player1, player2, player1_socket, player2_socket):
        threading.Thread.__init__(self)
        self.session_id = session_id
        self.player1 = player1
        self.player2 = player2
        self.player1_socket = player1_socket
        self.player2_socket = player2_socket

        self.started = False

        # ship placement
        self.occupied = {
            1: [],
            2: []
        }

        # player ready status
        self.ready = {
            1: False,
            2: False
        }

        # current player's turn
        self.turn = 1

        # current turn count
        self.turn_count = 1


    def startbattle(self):
        if self.started:
            return
        # send TURN to p1
        self.player1_socket["challenge"].send(b"TURN")
        # send WAIT to p2
        self.player2_socket["challenge"].send(b"WAIT")
        self.started = True

    def check_player(self, player_name):
        if player_name == self.player1.name:
            return 1
        if player_name == self.player2.name:
            return 2
        return False

    def is_turn(self, player):
        return self.turn == player

    def switch_turn(self):
        if self.turn == 1:
            self.turn = 2
            # send TURN to p2
            self.player2_socket["challenge"].send(b"TURN")
            # send WAIT to p1
            self.player1_socket["challenge"].send(b"WAIT")
        else:
            self.turn = 1
            # send TURN to p1
            self.player1_socket["challenge"].send(b"TURN")
            # send WAIT to p2
            self.player2_socket["challenge"].send(b"WAIT")

    def is_opponent_ready(self, player):
        if player == 1:
            return self.ready[2]
        else:
            return self.ready[1]

    def is_hit(self, player, coor):
        if player == 1:
            return coor in self.occupied[2]
        if player == 2:
            return coor in self.occupied[1]


class ClientThread(threading.Thread):
    def __init__(self, sock: socket, address: tuple, player_list: dict,
                 socket_list: dict, battle_list: dict):
        threading.Thread.__init__(self)
        self.sock = sock
        self.address = address
        self.live = True
        self.player_list = player_list
        self.socket_list = socket_list
        self.battle_list = battle_list

        # teje: butuh array buat simpan posisi kapal player
        # mockup: self.occupied, ClientThread.getPlayerShipPosition(), BattleshipServer.isLose()
        # Attack Procedure
        # 1. player attack, get atk coordinate X
        # 2. server check if X in self.occupied['enemy'], if yes remove it from self.occupied['enemy']
        # 3. server run isLose() function to check win/lose condition. If true send win/lose signal to clients
        #    If not, proceed to 4.
        # 4. send X to enemy to be drawn on their own board
        # 5. change turn

        # self.occupied = dict()
        # self.occupied.update({'p1': []})
        # self.occupied.update({'p2': []})

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
            if command == "HSCO":
                print(self.highscore())
            if command == "BTLS":
                print(self.battle(argument))
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

        # create new battle session
        bsid = str(len(self.battle_list)*17+1)
        bs = BattleSession(bsid, self.player_list[opponent], self.player,
                           self.socket_list[opponent], self.socket_list[self.player.name])
        self.battle_list[bsid] = bs

        msg = "BATL {} {} {}".format(opponent, self.player.name, bsid)
        self.socket_list[opponent]["main"].send("{} {}".format(msg, "1").encode())
        self.sock.send("{} {}".format(msg, "2").encode())

        # set status for both players
        self.player.goPlay()
        self.player_list[opponent].goPlay()

        return "293"

    def highscore(self):
        score_list = dbconn.get_highscore(self.conn)
        print(score_list)
        score_pickled = pickle.dumps(score_list)
        self.sock.send(score_pickled)
        return "295"

    def battle(self, bsid):
        bs = ''
        if bsid in self.battle_list:
            bs = self.battle_list[bsid]

        # check player
        as_player = bs.check_player(self.player.name)
        if as_player:
            self.sock.send(b"OK")
        else:
            self.sock.send(b"GOAWAY")

        # opponent's name
        opponent = ''
        if as_player == 1:
            opponent = bs.player2.name
        else:
            opponent = bs.player1.name

        # challenge sock
        o_csock = self.socket_list[opponent]["challenge"] # opponent's socket
        csock = self.socket_list[self.player.name]["challenge"] # self's socket

        # ship placing phase below
        data = self.sock.recv(1024)
        command, occupy = data.split(b" ")
        if command.decode() == "OCUP":
            bs.occupied[as_player] = pickle.loads(occupy)
            o_csock.send(b"ORDY")
            bs.ready[as_player] = True

        # wait for opponent ready
        print(self.player.name, "is waiting for", opponent, "to ready")
        while not bs.is_opponent_ready(as_player):
            pass
        print(opponent, "is readdy. Lets go")

        if as_player == 1:
            bs.startbattle()
        while True:
            # check if current turn
            while not bs.is_turn(as_player):
                pass # do nothing
            print("its", self.player.name, "turn")
            data = self.sock.recv(1024)
            data_splitted = data.decode().split()
            command, argument = data_splitted[0], " ".join(data_splitted[1:])
            # print(data_splitted)
            if command == "ATT":
                # print(self.player.name, "attacked", opponent, "on", "".join(self.convert_coordinate(argument)))
                # alpha, number = argument.split()
                if bs.is_hit(as_player, self.convert_coordinate(argument)):
                    csock.send("HIT {}".format(argument).encode())
                else:
                    csock.send("MISS {}".format(argument).encode())
                o_csock.send("ATTD {}".format(argument).encode())

            print("my turn is done", self.player.name)
            # switch turn
            bs.switch_turn()




    # def getPlayerShipPosition(self):
    #     # get player occupied tile. Get the data from scene_battle: BattleScene.occupied
    #     return

    # battle related method below

    def convert_coordinate(self, coor):
        alpha, number = coor.split()
        number = str((int(number)-40)//56 + 1)
        alpha = chr(65 + (int(alpha)-40)//56)
        return alpha+number

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
        self.battle_list = {}
        self.servwaiting = threading.Thread(target=self.waitForPlayer)
        self.csockwaiting = threading.Thread(target=self.pairChallengeSocket)
        self.servwaiting.start()
        self.csockwaiting.start()

    def waitForPlayer(self):
        print("Battleship Server is up. Waiting for player...")
        while True:
            conn, addr = self.servsock.accept()
            print("New connection initiated", addr)
            client = ClientThread(conn, addr, self.player_list, self.socket_list, self.battle_list)
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

    def isLose(self, player): # win/lose condition
        if self.occupied[player].__len__() == 0:
            return True
        return False
    

bsserver = BattleshipServer()

# try:
#     while True:
#         client_sock, addr = server_sock.accept()
#         client_thread = ClientThread(client_sock, addr)
#         client_thread.start()
# except KeyboardInterrupt:
#     pass

# server_sock.close()