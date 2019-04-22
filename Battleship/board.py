class Board:
    def __init__(self, sz=10):
        self.size = sz
        self.LEFT_MARGIN = 40
        self.RIGHT_MARGIN = 600
        self.TOP_MARGIN = 40
        self.BOTTOM_MARGIN = 600
        self.SQUARE_WIDTH = (self.RIGHT_MARGIN - self.LEFT_MARGIN) // self.size # #board square