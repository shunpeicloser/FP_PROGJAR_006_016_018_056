import pygame
import math

# constant
BOARD_SIZE = 19
KOMI = 6.5
BLACK = 0
WHITE = 1
STONE_WIDTH = 14
LEFTX_MARGIN = 37 - STONE_WIDTH
RIGHTX_MARGIN = 602 + STONE_WIDTH
TOPY_MARGIN = 39 - STONE_WIDTH
BOTY_MARGIN = 606 + STONE_WIDTH

XBOX_WIDTH = (RIGHTX_MARGIN - LEFTX_MARGIN) / (BOARD_SIZE)
YBOX_WIDTH = (BOTY_MARGIN - TOPY_MARGIN) / (BOARD_SIZE)

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.capture = 0
        self.area = 0
    
    def getname(self):
        return self.name

    def getcolorstr(self):
        if self.color == BLACK:
            return "Black"
        return "White"

def drawimage(screen, img, coordinate):
    if coordinate != None:
        screen.blit(img, coordinate)

def predictboardcoordinate(click_coordinate):
    # calculate nearest legal coordinate of board
    # return value is coordinate "x,y", None if it's deemed outside of board and sidebar
    ret = None

    nth_x = math.ceil((click_coordinate[0] - LEFTX_MARGIN) / XBOX_WIDTH)
    nth_y = math.ceil((click_coordinate[1] - TOPY_MARGIN) / YBOX_WIDTH)

    if nth_x > BOARD_SIZE or nth_y > BOARD_SIZE:
        return ret

    ret = ""
    if nth_x >= 9:
        nth_x += 1
    ret += str(chr(64 + nth_x) + ",")
    ret += str(20-nth_y)

    return ret

def boardtopixel(strcoor):
    if strcoor is None:
        return None
    xcoor = strcoor.split(",")[0]
    ycoor = strcoor.split(",")[1]

    # get the nth position of coordinate
    if ord(xcoor) >=ord("I"):
        xcoor = ord(xcoor) - 65
    else:
        xcoor = ord(xcoor) - 64
    
    ycoor = int(ycoor)

    # transform nth position into pixel coordinate
    xcoor = LEFTX_MARGIN + (xcoor - 1) * XBOX_WIDTH
    ycoor = TOPY_MARGIN + (20 - ycoor - 1) * YBOX_WIDTH

    return (xcoor, ycoor)

def main():
    p1 = Player("RECEH", BLACK)
    p2 = Player("TEJE", WHITE)
    pygame.init()
    pygame.display.set_caption(str(p1.getname()+"("+
                                p1.getcolorstr()+") vs "+
                                p2.getname()+"("+
                                p2.getcolorstr()+")"))
    
    # set display setting
    screen = pygame.display.set_mode((900, 640))
    
    # load needed image
    board_img = pygame.image.load("go-board1.png")
    sidebar_img = pygame.image.load("sidebar.png")
    black_piece = pygame.image.load("black.png")
    white_piece = pygame.image.load("white.png")

    running = True

    drawimage(screen, sidebar_img, (640, 0))
    drawimage(screen, board_img, (0, 0))

    pygame.display.update() 

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # draw board and sidebar
            drawimage(screen, sidebar_img, (640, 0))
            drawimage(screen, board_img, (0, 0))

            if event.type == pygame.MOUSEBUTTONUP:
                coor = predictboardcoordinate(pygame.mouse.get_pos())
                coor = boardtopixel(coor)
                print(coor)
                drawimage(screen, black_piece, coor)

                # update screen
                pygame.display.update()        

if __name__ == "__main__":
    main()