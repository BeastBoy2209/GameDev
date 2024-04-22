import pygame, sys, random
from pygame.locals import *
from .constants import GameConstants
game_constants = GameConstants()
# Create the constants (go ahead and experiment with different values)
BOARDWIDTH = 4  # number of columns in the board
BOARDHEIGHT = 4 # number of rows in the board
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 120
BLANK = None
#                 R    G    B
BLACK =         (  50,   50,   50)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
GRAY =          (  122,  122,  122)
BLUE =          (  112,  50, 255)
PURPLE =         (  186, 85, 211)
RED =           (255, 0, 0)
BGCOLOR = GRAY
TILECOLOR = BLACK
TEXTCOLOR = WHITE
BORDERCOLOR = RED
BASICFONTSIZE = 20
TEXT = PURPLE

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')

    # Remove NEW_SURF, NEW_RECT creation
    SOLVE_SURF, SOLVE_RECT = makeText('Solve', TEXT, BGCOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 250)

    mainBoard, solutionSeq = generateNewPuzzle(80)
    SOLVEDBOARD = getStartingBoard()
    allMoves = []
    WIN = False

    while True:
        slideTo = None
        msg = 'Click tile or press arrow keys to slide.'
        if mainBoard == SOLVEDBOARD:
            msg = 'Unlocked!'
            WIN = True
        drawBoard(mainBoard, msg) 
        checkForQuit()
        for event in pygame.event.get(): 
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                if (spotx, spoty) == (None, None):
                    if SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves) 
                        allMoves = []
                else:

                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN

        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8) 
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) 
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): 
        terminate() 
    for event in pygame.event.get(KEYUP): 
        if event.key == K_ESCAPE:
            terminate() 
        pygame.event.post(event) 


def getStartingBoard():
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
    return board


def getBlankPosition(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    validMoves = [UP, DOWN, LEFT, RIGHT]

    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, screen, game_constants, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(screen, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    BASICFONT = pygame.font.Font('data\dialogs\Grand9K Pixel.ttf', BASICFONTSIZE)
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    screen.blit(textSurf, textRect) 


def makeText(text, color, bgcolor, top, left):
    BASICFONT = pygame.font.Font('data\dialogs\Grand9K Pixel.ttf', BASICFONTSIZE) 
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def drawBoard(board, message, screen, game_constants):
    BGCOLOR = GRAY
    screen.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        screen.blit(textSurf, textRect) 

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley], screen=screen, game_constants=game_constants)

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(screen, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4) 

    # Инициализация SOLVE_SURF и SOLVE_RECT
    TEXT = PURPLE
    BGCOLOR = GRAY
    SOLVE_SURF, SOLVE_RECT = makeText('Solve', TEXT, BGCOLOR, 
                                      1900 - 120, 1000 - 250)
    screen.blit(SOLVE_SURF, SOLVE_RECT)

def slideAnimation(board, direction, message, animationSpeed, screen, game_constants):
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    drawBoard(board, message, screen, game_constants)
    baseSurf = screen.copy() 
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        checkForQuit()
        screen.blit(baseSurf, (0, 0)) 
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], screen, game_constants, adjy=-i)  
        elif direction == DOWN:
            drawTile(movex, movey, board[movex][movey], screen, game_constants, adjy=i) 
        elif direction == LEFT:
            drawTile(movex, movey, board[movex][movey], screen, game_constants, adjx=-i) 
        elif direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], screen, game_constants, adjx=i) 

        pygame.display.update()


def generateNewPuzzle(numSlides, screen, game_constants):
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '', screen, game_constants)
    pygame.display.update()
    pygame.time.wait(500) 
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new code...', int(TILESIZE / 3), screen, game_constants)
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves, screen, game_constants):
    revAllMoves = allMoves[:] 
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '', int(TILESIZE / 2), screen, game_constants)
        makeMove(board, oppositeMove)


if __name__ == '__main__':
    main()