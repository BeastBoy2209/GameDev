import pygame

pygame.init()

class GameConstants:

    def __init__(self): 
        # Параметры окна
        WINDOWWIDTH = 1900
        WINDOWHEIGHT = 1000
        FPS = 120

        # Цвета
        BLACK = (50, 50, 50)
        WHITE = (255, 255, 255)
        BRIGHTBLUE = (0, 50, 255)
        GRAY = (122, 122, 122)
        BLUE = (112, 50, 255)
        PURPLE = (186, 85, 211)
        RED = (255, 0, 0)
        TEXT = PURPLE 
        BGCOLOR = GRAY
        TILECOLOR = BLACK
        TEXTCOLOR = WHITE
        BORDERCOLOR = RED

        # Шрифт
        BASICFONTSIZE = 20
        BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

        # Параметры игры в сейф
        BOARDWIDTH = 4
        BOARDHEIGHT = 4
        TILESIZE = 80
        XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
        YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
        BLANK = None

        # Направления
        UP = 'up'
        DOWN = 'down'
        LEFT = 'left'
        RIGHT = 'right'