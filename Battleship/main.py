import pygame
import scene_login
import scene_register
import scene_room
import scene_battle
import board
import control
import scene_highscore
import scene_lobby2

import threading
from queue import Queue

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 9000))
welcome = sock.recv(1024).decode()
if welcome:
    print("Connected to server yay :D")

challenge_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# import player
# the_player = player.Player("")

class SocketListener(threading.Thread):
    def __init__(self, sock, q):
        threading.Thread.__init__(self)
        self.q = q
        self.sock = sock
        self.daemon = True
        print("here we go listener")
    def run(self):
        try:
            while True:
                data = self.sock.recv(1024)
                self.q.put(data.decode())
        except ConnectionAbortedError:
            print("Exiting socket listener...")
            return
q = Queue()

gamestatus = 1
ls = scene_login.LoginScene(sock, challenge_sock)
regs = scene_register.RegisterScene(sock)
rs = scene_room.RoomScene(sock)
bs = scene_battle.BattleScene(board.Board(10), control.Control(), sock, q)
hs = scene_highscore.HighscoreScene(sock)
lbs = scene_lobby2.LobbyScene(sock, q)
while gamestatus > 0:
    if gamestatus == 1:
        gamestatus = ls.run()
        a = SocketListener(challenge_sock, q)
        a.start()
    if gamestatus == 2:
        gamestatus = regs.run()
    if gamestatus == 3:
        gamestatus = rs.run()
    if gamestatus == 4:
        gamestatus = bs.run()
    if gamestatus == 5:
        gamestatus = hs.run()
    if gamestatus == 6:
        gamestatus = lbs.run()

# quiting
sock.send(b"QUIT")
sock.close()
challenge_sock.close()
