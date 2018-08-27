# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license
#
#
# Pathfinding algorithm
# By Peter Bocz
# github.com:analphagamma

import random, pygame, sys
import pathfinder as pf
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
NO_OF_OBSTACLES = 15 * 0.01 * CELLWIDTH * CELLSIZE

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    while True:
        runGame()
        showGameOverScreen(deathmessage)

def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Generate blocked cells
    obstacles = generateObstacles(NO_OF_OBSTACLES)
    # Start the apple in a random place.
    apple = getRandomLocation()
    # Instantiating board object
    board = pf.Board(CELLWIDTH, CELLHEIGHT)
    for loc in obstacles:
       board.cell_block((loc['x'], loc['y']))
    
    while True: # main game loop

        global deathmessage
        # making the snake's position blocked cells
        for loc in wormCoords:
            board.cell_block((loc['x'], loc['y']))

        # calculating shortest route from wormhead to apple
        route = pf.Route(board)
        try:
            to_apple = route.FindShortestPathBFS((wormCoords[HEAD]['x'], wormCoords[HEAD]['y']), (apple['x'], apple['y']))[1]
        except:
            to_apple = (apple['x'], apple['y']) # worm's next to apple

        # check if the worm has the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            print(deathmessage)
            return # game over
        # check if worm has hit an obstacle
        for obstacle in obstacles:
            if wormCoords[HEAD]['x'] == obstacle['x'] and wormCoords[HEAD]['y'] == obstacle['y']:
                print(deathmessage)
                return # game over
        # check if worm has hit itself
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                print(deathmessage)
                return # game over


        if (to_apple[0] > wormCoords[HEAD]['x'] and to_apple[1] == wormCoords[HEAD]['y']) and direction != LEFT:
            direction = RIGHT
        elif (to_apple[0] < wormCoords[HEAD]['x'] and to_apple[1] == wormCoords[HEAD]['y']) and direction != RIGHT:
            direction = LEFT
        elif (to_apple[0] == wormCoords[HEAD]['x'] and to_apple[1] > wormCoords[HEAD]['y']) and direction != UP:
            direction = DOWN
        elif (to_apple[0] == wormCoords[HEAD]['x'] and to_apple[1] < wormCoords[HEAD]['y']) and direction != DOWN:
            direction = UP
        else:
            opposite_directions = {LEFT: RIGHT, RIGHT: LEFT, UP: DOWN, DOWN: UP}
            all_directions = [LEFT, RIGHT, UP, DOWN]
            all_directions.remove(opposite_directions[direction])
            direction = random.choice(all_directions)


        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)

        # check if the worm has the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            deathmessage = '"I hit the wall!"'
            print(deathmessage)
            return # game over
        # check if worm has hit an obstacle
        for obstacle in obstacles:
            if wormCoords[HEAD]['x'] == obstacle['x'] and wormCoords[HEAD]['y'] == obstacle['y']:
                deathmessage = '"I hit an obstacle!"'
                print(deathmessage)
                return # game over
        # check if worm has hit itself
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                deathmessage = '"I bit myself!"' # This shouldn't happen
                print(deathmessage)
                return # game over

         # resetting blocked cells
        for loc in wormCoords:
            board.cell_unblock((loc['x'], loc['y']))

        # check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            while apple in wormCoords or apple in obstacles:
                apple = getRandomLocation() # set a new apple somewhere
        else:
            del wormCoords[-1] # remove worm's tail segment
        
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawObstacles(obstacles)
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def terminate():
    pygame.quit()
    sys.exit()

def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def generateObstacles(amount):
    obstacles = []
    while len(obstacles) < amount:
        randloc = getRandomLocation()
        if randloc not in obstacles:
            obstacles.append(randloc)
    return obstacles

def showGameOverScreen(message):
    gameOverFont = pygame.font.Font('freesansbold.ttf', 60)
    messageSurf = gameOverFont.render(message, True, RED)
    messageRect = messageSurf.get_rect()
    messageRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    
    DISPLAYSURF.blit(messageSurf, messageRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Length: %s' % (score), True, RED)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, BLACK, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)

def drawObstacles(blockCoords):
    for coord in blockCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        blockRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, WHITE, blockRect)

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
