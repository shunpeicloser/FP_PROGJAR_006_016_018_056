import pygame

class Control:
    NO_ACTION = 0
    IS_PLACINGSHIP = 1

    def __init__(self):
        self.mousestatus = self.NO_ACTION
        self.selectedbattleship = 'carrier' # set to None for Production

    def getboardcoordinate(self, board, coordinate):
        if board != None and coordinate != None:
            x = (coordinate[0] - board.LEFT_MARGIN) // board.SQUARE_WIDTH
            y = (coordinate[1] - board.TOP_MARGIN) // board.SQUARE_WIDTH
            x, y = chr(65 + x), y + 1
            if (ord(x) >= ord('A') and ord(x) <= ord('J')) and (y >= 1 and y <= 10):
                return (x, y)
        else:
            return None

    def getpixelcoordinate(self, board, boardcoor): # get right-bottom of square, for placing ship
        if board != None and boardcoor != None:
            x = board.LEFT_MARGIN + (ord(boardcoor[0]) - 65) * board.SQUARE_WIDTH + board.SQUARE_WIDTH
            y = board.TOP_MARGIN + (boardcoor[1] - 1) * board.SQUARE_WIDTH + board.SQUARE_WIDTH
            return (x, y)
        else:
            return None