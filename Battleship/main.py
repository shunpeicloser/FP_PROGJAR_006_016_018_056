import pygame
import scene_login
import scene_battle
import board
import control

gamestatus = 1
ls = scene_login.LoginScene()
bs = scene_battle.BattleScene(board.Board(10), control.Control())
while gamestatus > 0:
    if gamestatus == 1:
        gamestatus = ls.run()
    if gamestatus == 4:
        gamestatus = bs.run()
