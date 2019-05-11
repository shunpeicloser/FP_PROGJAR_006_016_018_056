import pygame
import scene_login
import scene_register
import scene_room
import scene_battle
import board
import control
import scene_highscore
import scene_lobby

gamestatus = 6
ls = scene_login.LoginScene()
regs = scene_register.RegisterScene()
rs = scene_room.RoomScene()
bs = scene_battle.BattleScene(board.Board(10), control.Control())
hs = scene_highscore.HighscoreScene()
lbs = scene_lobby.LobbyScene()
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
