import pygame
import math


def addLife(r, c):
    grid[r * cols + c] = 1
    life.add(r * cols + c)
    undo.append(r * cols + c)


def checkLife():
    death.clear()
    p_life.clear()
    for i in life:
        count = 0
        c_row = math.floor(i / cols)
        c_col = i % cols
        for r in range(c_row - 1, c_row + 2):
            for c in range(c_col - 1, c_col + 2):
                if r == c_row and c == c_col:
                    continue
                if grid[r * cols + c] == 1:
                    count += 1
                else:
                    if r * cols + c in p_life:
                        p_life.update({r * cols + c: p_life.get(r * cols + c) + 1})
                    else:
                        p_life.update({r * cols + c: 1})
        if count < 2 or count > 3:
            death.add(i)


def createLife():
    for key in p_life:
        if p_life.get(key) == 3:
            life.add(key)
            grid[key] = 1


def die():
    for i in death:
        life.remove(i)
        grid[i] = 0


def sequence():
    checkLife()
    die()
    createLife()


pygame.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1400
FRAME_RATE = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game')
# ----------------------------------------
rows = 10000
cols = 10000
height = 100
width = 100
origin_r = int(rows / 2 - height / 2)
origin_c = int(cols / 2 - width / 2)

grid = [0] * (rows * cols)
life = set()
death = set()
p_life = {}
ready = False
undo = []
mDown = False

# ----------------------------------------

tick = 0
simu_rate = 3
run = True
while run:
    clock.tick(FRAME_RATE)
    screen.fill((0, 0, 0))

    # ----------------------------------------
    for r in range(int(rows / 2 - height / 2), int(rows / 2 + height/2)):
        for c in range(int(cols / 2 - width / 2), int(cols / 2 + width/2)):
            if (r * rows + c) in life:
                pygame.draw.rect(screen, (255, 255, 255), ((c - origin_c) * 14 + 1,
                                                           (r - origin_r) * 14 + 1, 12, 12))
    if ready:
        tick += 1
        if tick % simu_rate == 0:
            sequence()
    else:
        x, y = pygame.mouse.get_pos()
        c = x - x % 14 + 1
        r = y - y % 14 + 1
        pygame.draw.rect(screen, (160, 160, 160), (c, r, 12, 12))

    if mDown:
        addLife(int(r / 14) + origin_r, int(c / 14) + origin_c)

    # ----------------------------------------


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE and not ready:
                ready = True
                mDown = False
            if event.key == pygame.K_z and not ready:
                if len(undo) > 0:
                    grid[undo[0]] = 0
                    life.remove(undo[0])
                    del undo[0]
        if event.type == pygame.MOUSEBUTTONDOWN and not ready:
            mDown = True
        if event.type == pygame.MOUSEBUTTONUP and not ready:
            mDown = False
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
