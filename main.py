import math
import random
import time

import pygame

inf = float("inf")
map_size = 400
path_tabel_size = 980
min_point_distance = 40
point_size = 17
s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
size = 5
joints = [[1 if random.random() > 0.1 and i != k else 0 for k in range(size)] for i in range(size)]
weights = [[random.randrange(1, 10) if joints[i][k] else inf  for k in range(size)] for i in range(size)]
history = [[k if joints[i][k] else 0 for k in range(size)] for i in range(size)]
nodes = list(filter(lambda x: x is not None, [[x, y] if joints[y][x] else None for x in range(size) for y in range(size)]))

def generate_new():
    global joints, weights, history, nodes
    joints = [[1 if random.random() > 0.1 and i != k else 0 for k in range(size)] for i in range(size)]
    weights = [[random.randrange(1, 10) if joints[i][k] else inf for k in range(size)] for i in range(size)]
    history = [[k if joints[i][k] else 0 for k in range(size)] for i in range(size)]
    nodes = list(filter(lambda x: x is not None, [[x, y] if joints[y][x] else None for x in range(size) for y in range(size)]))


screen = pygame.display.set_mode((0, 0))
pygame.display.toggle_fullscreen()
pygame.font.init()
my_font = pygame.font.SysFont('C059 Bold', 50)
pygame.init()

def drawPath(path):
    pygame.draw.lines(screen, (0, 0, 0), False, path, 1)

def generate_weight_matrix():
    block = pygame.Surface((map_size + 4, map_size + 4))
    block.fill((255, 255, 255))
    cell_size = map_size / (size + 1)

    pygame.draw.rect(block, (125, 255, 125), ((cell_size, 0), (map_size - cell_size + 2, cell_size)))
    pygame.draw.rect(block, (125, 255, 125), ((0, cell_size), (cell_size, map_size - cell_size + 2)))

    for j in range(size + 1):
        pygame.draw.rect(block, (255, 200, 200), ((j * cell_size, j * cell_size), (cell_size + 1, cell_size + 1)))

    for i in range(size + 2):
        pygame.draw.line(block, (0, 0, 0), (i * cell_size, 0), (i * cell_size, map_size), width=2)
        pygame.draw.line(block, (0, 0, 0), (0, i * cell_size), (map_size, i * cell_size), width=2)


    for y in range(size + 1):
        for x in range(size + 1):
            if y == 0 and x != 0:
                text_surface = my_font.render(s[x - 1], False, (0, 0, 0))
                block.blit(text_surface, (x * cell_size + 20, y * cell_size + 20))

            if x == 0 and y != 0:
                text_surface = my_font.render(s[y - 1], False, (0, 0, 0))
                block.blit(text_surface, (x * cell_size + 20, y * cell_size + 20))

    for cords in nodes:
        if weights[cords[1]][cords[0]] != inf:
            pygame.draw.circle(block, (200, 200, 255), ((cords[0] + 2) * cell_size - cell_size / 2 + 1, (cords[1] + 2) * cell_size - cell_size / 2 + 1), cell_size / 2 - 4)
            text_surface = my_font.render(str(weights[cords[1]][cords[0]]), False, (0, 0, 0))
            block.blit(text_surface, ((cords[0] + 1) * cell_size + 26, (cords[1] + 1) * cell_size + 20))


    return block


def get_random_point_on_circle(x0, y0, R):
    x = x0 + R * math.cos(random.random() * math.pi * 2)
    y = y0 + R * math.sin(random.random() * math.pi * 2)
    print(x, y)
    return [x, y]

def draw_paths(_weights):
    block = pygame.Surface((path_tabel_size, path_tabel_size))

    block.fill((200, 200, 200))

    i = 0
    w = 100
    for _out in range(size):
        for _to in range(size):
            if _weights[_out][_to] != inf:
                i+=1
                pygame.draw.line(block, (0, 0, 255), (point_size + 10, (point_size * 2 + 10) * i),
                                 (point_size + w, (point_size * 2 + 10) * i), 10)
                pygame.draw.circle(block, (255, 0, 0), (point_size + 10, (point_size * 2 + 10) * i), point_size)
                pygame.draw.circle(block, (255, 0, 0), (point_size + 10 + w, (point_size * 2 + 10) * i), point_size)

                font = pygame.font.SysFont('C059 Bold', point_size * 2)
                text_surface = font.render(s[_out], False, (255, 255, 255))
                block.blit(text_surface, (point_size + 3, (point_size * 2 + 10) * i - 10))

                text_surface = font.render(s[_to], False, (255, 255, 255))
                block.blit(text_surface, (point_size + 3 + w, (point_size * 2 + 10) * i - 10))

                pygame.draw.rect(block, (0, 255, 0), (
                    (
                        point_size + 10 + w / 2 - point_size,
                        (point_size * 2 + 10) * i  - point_size
                    ),
                    (
                        point_size * 2,
                        point_size * 2
                    )
                ))

                font = pygame.font.SysFont('C059 Bold', point_size * 2)
                text_surface = font.render(str(_weights[_out][_to]), False, (0, 0, 0))
                block.blit(text_surface, (point_size + 3 + w / 2 + 2, (point_size * 2 + 10) * i - 10))

    return block


def solve():
    for A in range(size):
        for B in range(size):
            if weights[A][B] != inf:
                for C in range(size):
                    if weights[A][C] > weights[A][B] + weights[B][C]:
                        weights[A][C] = weights[A][B] + weights[B][C]
                        history[A][C] = history[A][B]

def draw_mapa():
    block = pygame.Surface((path_tabel_size, path_tabel_size))
    block.fill((150, 200, 200))

    mapa = [[random.randrange(point_size * 2, path_tabel_size - point_size * 2) for i in range(2)] for k in range(size)]

    for i in range(size):
        for j in range(size):
            color = (255, 0, 255)
            offset = -5
            if i >= j:
                color = (0, 0, 255)
                offset = 5

            pygame.draw.line(block, color, [mapa[i][0] + offset, mapa[i][1] + offset], [mapa[j][0] + offset, mapa[j][1] + offset], 3)

    for i in range(size):
        for j in range(size):
            offset = -10
            if i >= j:
                offset = 10

            x = (mapa[i][0] + mapa[j][0]) / 2
            y = (mapa[i][1] + offset + mapa[j][1] + offset) / 2

            font = pygame.font.SysFont('C059 Bold', point_size * 2)
            text_surface = font.render(str(weights[i][j]), False, (0, 0, 0))
            block.blit(text_surface, (x, y))


    for k in range(size):
        pygame.draw.circle(block, (255, 255, 255), mapa[k], point_size)
        font = pygame.font.SysFont('C059 Bold', point_size * 2)
        text_surface = font.render(s[k], False, (0, 0, 0))
        block.blit(text_surface, [mapa[k][0] - point_size / 2, mapa[k][1] - point_size / 2])


    return block


def update():
    screen.fill((255, 255, 255))
    screen.blit(generate_weight_matrix(), (50, 50))
    screen.blit(draw_paths(weights), (500, 50))
    solve()
    screen.blit(draw_paths(weights), (700, 50))
    screen.blit(draw_mapa(), (900, 50))
    pygame.display.flip()

update()
print(sum(arr) / len(arr))
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            generate_new()
            update()