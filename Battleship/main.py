import pygame
import scene_login
import scene_register
import scene_room
import scene_battle
import board
import control

gamestatus = 1
ls = scene_login.LoginScene()
regs = scene_register.RegisterScene()
rs = scene_room.RoomScene()
bs = scene_battle.BattleScene(board.Board(10), control.Control())
while gamestatus > 0:
    if gamestatus == 1:
        gamestatus = ls.run()
    if gamestatus == 2:
        gamestatus = regs.run()
    if gamestatus == 3:
        gamestatus = rs.run()
    if gamestatus == 4:
        gamestatus = bs.run()
