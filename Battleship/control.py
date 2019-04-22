import pygame

class Control:
    def getboardcoordinate(self, board, coordinate):
        x = (coordinate[0] - board.LEFT_MARGIN) // board.SQUARE_WIDTH
        y = (coordinate[1] - board.TOP_MARGIN) // board.SQUARE_WIDTH
        x, y = chr(65 + x), y + 1
        return (x, y)
    
    def getpixelcoordinate(self, board, boardcoor): # get right-bottom of square, for placing ship
        x = board.LEFT_MARGIN + (ord(boardcoor[0]) - 65) * board.SQUARE_WIDTH + board.SQUARE_WIDTH
        y = board.TOP_MARGIN + (boardcoor[1] - 1) * board.SQUARE_WIDTH + board.SQUARE_WIDTH
        return (x, y)