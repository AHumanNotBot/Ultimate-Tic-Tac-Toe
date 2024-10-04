import sys
import pygame
from pygame.locals import *
import math

# Global variables
gameturn = False
gameGrids = [[[0, 0, 0] for _ in range(3)] for _ in range(9)]
miniGameWon = [False] * 9
wonBoxList = []
counterPlaceholder = False
nextBox = 0
bigGrid = [[0, 0, 0] for _ in range(3)]
restrictedBox = 10
coordslist = []
imglist = []

# Pygame initialization
pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 400))
font = pygame.font.Font("freesansbold.ttf", 20)

# Load images
imgX = pygame.image.load("tttX.png")
imgX = pygame.transform.smoothscale(imgX, (25, 25))
imgBIGX = pygame.transform.smoothscale(imgX, (90, 90))

imgO = pygame.image.load("tttO.png")
imgO = pygame.transform.smoothscale(imgO, (25, 25))
imgBIGO = pygame.transform.smoothscale(imgO, (90, 90))

startImg = pygame.image.load("StartScreen.png")
startTxt = pygame.image.load("StartText.png")
startTxt= pygame.transform.smoothscale(startTxt, (300,75))


# Positions of small grids
gamePosKey = {
    1: pygame.Rect(0, 0, 85, 85),
    2: pygame.Rect(100, 0, 85, 85),
    3: pygame.Rect(200, 0, 85, 85),
    4: pygame.Rect(0, 100, 85, 85),
    5: pygame.Rect(100, 100, 85, 85),
    6: pygame.Rect(200, 100, 85, 85),
    7: pygame.Rect(0, 200, 85, 85),
    8: pygame.Rect(100, 200, 85, 85),
    9: pygame.Rect(200, 200, 85, 85)
}

def disp3x3(Xoffset, Yoffset):
    for sRow in range(3):
        for sCol in range(3):
            pygame.draw.rect(DISPLAYSURF, (255, 255, 255),
                             ((Xoffset * 100 + sRow * 30),
                              (Yoffset * 100 + sCol * 30), 25, 25))

def dispBoard():
    DISPLAYSURF.fill((0, 0, 0))
    for bRow in range(3):
        for bCol in range(3):
            disp3x3(bRow, bCol)

def letterPos(x, y):
  xplc = 30 * (x // 30)
  yplc = 30 * (y // 30)
  xDif = 0
  yDif = 0
  if x >= 90:
    if x <= 100:
      xplc = 60
    elif x < 190:
      xplc = 30 * ((x - 10) // 30) + 10
      xDif = 10
  if x >= 190:
    if x < 200:
      xplc = 160
      xDif = 10
    elif x <= 290:
      xplc = 30 * ((x - 20) // 30) + 20
      xDif = 20
  if y >= 90:
    if y <= 100:
      yplc = 60
    elif y < 190:
      yplc = 30 * ((y - 10) // 30) + 10
      yDif = 10
  if y >= 190:
    if y < 200:
      yplc = 160
      yDif = 10
    elif y <= 290:
      yplc = 30 * ((y - 20) // 30) + 20
      yDif = 20
  return xplc, yplc, xDif, yDif

def dispLetter():
    for i in range(len(coordslist)):
        DISPLAYSURF.blit(imglist[i], coordslist[i])

def checkwins(grid):
  checkList = [0, 0, 0]
  checkList2 = [0, 0, 0]
  for row in range(len(grid)):
    if all(x == 1 for x in grid[row]):
      return 1

    if all(x == 2 for x in grid[row]):
      return 2

    for collumn in range(len(grid[row])):
      if grid[0][collumn] == 1 and grid[1][collumn] == 1 and grid[2][
          collumn] == 1:
        return 1

      if grid[0][collumn] == 2 and grid[1][collumn] == 2 and grid[2][
          collumn] == 2:
        return 2
  for x in range(3):
    checkList[x] = grid[x][x]
    checkList2[x] = grid[x][2 - x]

  if all(num == 1 for num in checkList2):
    return 1

  if all(num == 2 for num in checkList2):
    return 2

  if all(num == 1 for num in checkList):
    return 1

  if all(num == 2 for num in checkList):
    return 2
def start_screen(startTxt):
  while True:
      for event in pygame.event.get():
          if event.type == QUIT:
              pygame.quit()
              sys.exit()
          if event.type == MOUSEBUTTONDOWN:
              x, y = pygame.mouse.get_pos()
              if 50 <= x <= 350 and 240 <= y <= 310:
                  return

      # Clear the screen
      DISPLAYSURF.fill((255, 255, 255))

      # Calculate the scaling factor, with adjusted frequency and phase shift
      t = pygame.time.get_ticks() / 1000
      frequency = 2  # Adjust this value as needed
      phase_shift = math.pi / 2  # 90 degrees phase shift to start the cycle at the smallest size
      scaling_factor = max(0.5, 1 + 0.5 * math.cos(frequency * t + phase_shift))

      # Scale the image
      scaled_startTxt = pygame.transform.smoothscale(startTxt, (int(startTxt.get_width() * scaling_factor), int(startTxt.get_height() * scaling_factor)))

      # Get the new rect and set its center
      scaled_startTxt_rect = scaled_startTxt.get_rect()
      scaled_startTxt_rect.center = (DISPLAYSURF.get_width() // 2, 240 + startTxt.get_height() // 2)

      # Blit the background image first
      DISPLAYSURF.blit(startImg, (0, 0))

      # Now, blit the scaled image at the new rect position
      DISPLAYSURF.blit(scaled_startTxt, scaled_startTxt_rect.topleft)

      pygame.display.update()

# Main game loop
start_screen(startTxt)
dispBoard()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            x = int(pygame.mouse.get_pos()[0])
            y = int(pygame.mouse.get_pos()[1])
            if x < 290 and y < 290:
                gameNum = int(x / 100) + 3 * int(y / 100)
                bigRow = int(x / 100) + 1
                bigCol = int(y / 100) + 1
                xp, yp, xDif, yDif = letterPos(x, y)
                xDif, yDif = xDif * 10, yDif * 10
                plx, ply = int((xp - xDif) / 30), int((yp - yDif) / 30)
                bigBox = bigRow - 1 + 3 * (bigCol - 1)

                if gameGrids[gameNum][plx][ply] == 0:
                    if ((not counterPlaceholder or miniGameWon[nextBox]) or gameNum == nextBox) and not miniGameWon[bigBox]:
                        counterPlaceholder = True
                        nextBox = plx + 3 * ply
                        dispBoard()
                        img = imgO if gameturn else imgX
                        coordslist.append((xp, yp))
                        imglist.append(img)
                        gameGrids[gameNum][plx][ply] = int(gameturn) + 1

                        # Check for wins in mini grids
                        for i in range(0, 9):
                            if checkwins(gameGrids[i]) == 1 or checkwins(gameGrids[i]) == 2:
                                miniGameWon[i] = True
                                img = imgBIGX if checkwins(gameGrids[i]) == 1 else imgBIGO
                                coordslist.append(gamePosKey[i + 1].topleft)
                                imglist.append(img)

                        # Check for wins in the big grid
                        for i in range(1, 10):
                            if miniGameWon[nextBox]:
                                restrictedBox = nextBox
                                wonBoxList.append(nextBox)
                                if not wonBoxList.__contains__(i - 1):
                                    pygame.draw.rect(DISPLAYSURF, (0, 255, 0), gamePosKey[i], 5)
                            else:
                                restrictedBox = 10
                                pygame.draw.rect(DISPLAYSURF, (0, 255, 0), gamePosKey[nextBox + 1], 5)
                            if miniGameWon[i-1]:
                                x = i-1
                                bigGrid[x//3][x%3] = int(gameturn) + 1

                        # Switch turn
                        gameturn = not gameturn
                        pwon = checkwins(bigGrid)
                        if pwon == 1 or pwon == 2:
                            DISPLAYSURF.blit(font.render("Player {} ".format(pwon), True, (0, 0, 0), (250, 250, 0)), (290, 50))
                            DISPLAYSURF.blit(font.render("WINS ", True, (0, 0, 0), (250, 250, 0)), (290, 70))
                        dispLetter()
                    else:
                        DISPLAYSURF.blit(font.render("INVALID", True, (255, 0, 0)), (290, 200))
                        DISPLAYSURF.blit(font.render("MOVE", True, (255, 0, 0)), (290, 220))

    # Display player's turn
    DISPLAYSURF.blit(font.render("Player {}'s ".format(int(gameturn) + 1), True, (0, 0, 0), (255, 0, 0)), (290, 0))
    DISPLAYSURF.blit(font.render("turn", True, (0, 0, 0), (255, 0, 0)), (290, 20))

    pygame.display.update()

