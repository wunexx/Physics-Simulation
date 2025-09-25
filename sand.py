import pygame, random
from PIL import Image

pygame.init()

# set to any file name
img = Image.open("wizard.png").convert("L")

MAX_SIZE = (300, 300)

img.thumbnail(MAX_SIZE)

WIDTH, HEIGHT = img.size

AIR, SAND, WATER, GAS, STONE, ACID = 0, 1, 2, 3, 4, 5
CELLSIZE = 3

screen = pygame.display.set_mode((WIDTH * CELLSIZE, HEIGHT * CELLSIZE))
pygame.display.set_caption("Sand Simulation")

grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

for y in range(HEIGHT):
    for x in range(WIDTH):
        brightness = img.getpixel((x, y))
        if brightness < 42:
            grid[y][x] = AIR
        elif brightness < 84:
            grid[y][x] = WATER
        elif brightness < 126:
            grid[y][x] = SAND
        elif brightness < 168:
            grid[y][x] = STONE
        else:
            grid[y][x] = GAS

clock = pygame.time.Clock()

isPaused = True
isPlaying = True
 
while isPlaying:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isPlaying = False
        elif event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_SPACE):
                isPaused = not isPaused

    if isPaused == False:

        for y in range(HEIGHT - 2, -1, -1):
            for x in range(WIDTH):
                cell = grid[y][x]

                # ------------------ SAND ------------------
                if cell == SAND:
                    if y + 1 < HEIGHT and grid[y + 1][x] in (AIR, WATER, GAS):
                        grid[y + 1][x], grid[y][x] = grid[y][x], grid[y + 1][x]
                    else:
                        dirs = [-1, 1]
                        random.shuffle(dirs)
                        for dx in dirs:
                            nx = x + dx
                            ny = y + 1
                            if 0 <= nx < WIDTH and ny < HEIGHT and grid[ny][nx] in (AIR, WATER, GAS):
                                grid[ny][nx], grid[y][x] = grid[y][x], grid[ny][nx]
                                break

                #------------------ WATER ------------------
                elif cell == WATER:
                    if y + 1 < HEIGHT and grid[y + 1][x] in (AIR, GAS):
                        grid[y + 1][x], grid[y][x] = grid[y][x], grid[y + 1][x]
                    else:
                        dirs = [-1, 1]
                        random.shuffle(dirs)
                        moved = False
                        for dx in dirs:
                            nx = x + dx
                            ny = y + 1
                            if 0 <= nx < WIDTH and ny < HEIGHT and grid[ny][nx] in (AIR, GAS):
                                grid[ny][nx], grid[y][x] = grid[y][x], grid[ny][nx]
                                moved = True
                                break
                        if not moved:
                            for dx in dirs:
                                nx = x + dx
                                if 0 <= nx < WIDTH and grid[y][nx] == AIR:
                                    grid[y][nx], grid[y][x] = grid[y][x], grid[y][nx]
                                    break

                #------------------ ACID ------------------
                elif cell == ACID:
                    if y + 1 < HEIGHT and grid[y + 1][x] in (AIR, GAS, WATER):
                        grid[y + 1][x], grid[y][x] = grid[y][x], grid[y + 1][x]
                    elif  y + 1 < HEIGHT and grid[y + 1][x] == STONE:
                        grid[y + 1][x] = ACID
                        grid[y][x] == AIR
                    else:
                        dirs = [-1, 1]
                        random.shuffle(dirs)
                        moved = False
                        for dx in dirs:
                            nx = x + dx
                            ny = y + 1
                            if 0 <= nx < WIDTH and ny < HEIGHT and grid[ny][nx] in (AIR, GAS):
                                grid[ny][nx], grid[y][x] = grid[y][x], grid[ny][nx]
                                moved = True
                                break
                            elif 0 <= nx < WIDTH and ny < HEIGHT and grid[ny][nx] == STONE:
                                grid[ny][nx] = ACID
                                grid[y][x] = AIR
                                moved = True
                                break
                        if not moved:
                            for dx in dirs:
                                nx = x + dx
                                if 0 <= nx < WIDTH and grid[y][nx] in (AIR, GAS):
                                    grid[y][nx], grid[y][x] = grid[y][x], grid[y][nx]
                                    break
                                elif 0 <= nx < WIDTH and grid[y][nx] == STONE:
                                    grid [y][nx] = ACID
                                    grid[y][x] = AIR

        # ------------------ GAS (top-to-bottom) ------------------
        for y in range(1, HEIGHT):
            for x in range(WIDTH):
                if grid[y][x] == GAS:
                    if y - 1 >= 0 and grid[y - 1][x] == AIR:
                        grid[y - 1][x], grid[y][x] = grid[y][x], grid[y - 1][x]
                    else:
                        dirs = [-1, 1]
                        random.shuffle(dirs)
                        moved = False
                        for dx in dirs:
                            nx = x + dx
                            ny = y - 1
                            if 0 <= nx < WIDTH and ny >= 0 and grid[ny][nx] == AIR:
                                grid[ny][nx], grid[y][x] = grid[y][x], grid[ny][nx]
                                moved = True
                                break
                        if not moved:
                            for dx in dirs:
                                nx = x + dx
                                if 0 <= nx < WIDTH and grid[y][nx] == AIR:
                                    grid[y][nx], grid[y][x] = grid[y][x], grid[y][nx]
                                    break

    # ------------------ RENDERING ------------------

    screen.fill((0, 0, 0))
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] == SAND:
                color = (255, 255, 0)
            elif grid[y][x] == WATER:
                color = (150, 150, 255)
            elif grid[y][x] == GAS:
                color = (100, 100, 100)
            elif grid[y][x] == STONE:
                color = (50, 50, 50)
            elif grid[y][x] == ACID:
                color = (0, 255, 0)
            else:
                continue
            pygame.draw.rect(screen, color, (x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()