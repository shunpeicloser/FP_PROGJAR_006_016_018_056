import pygame
import scene_login
import scene_register
import scene_room
import scene_battle
import board
import control
import scene_highscore
import scene_lobby2

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 9000))
welcome = sock.recv(1024).decode()
if welcome:
    print("Connected to server yay :D")

gamestatus = 1
ls = scene_login.LoginScene(sock)
regs = scene_register.RegisterScene(sock)
rs = scene_room.RoomScene(sock)
bs = scene_battle.BattleScene(board.Board(10), control.Control(), sock)
hs = scene_highscore.HighscoreScene(sock)
lbs = scene_lobby2.LobbyScene(sock)
while gamestatus > 0:
    if gamestatus == 1:
        gamestatus = ls.run()
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
