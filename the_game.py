from random import choice, random
from colorama import Fore, Style
from os import system, name


def coloring(text, color):
    colors = {'r': Fore.RED, 'g': Fore.GREEN, 'b': Fore.BLUE, 'c': Fore.LIGHTCYAN_EX, 'w': Fore.WHITE}
    try:
        return colors[color] + text + Style.RESET_ALL
    except KeyError:
        return text


SIZE_X = 210
SIZE_Y = 50
DEAD = ' '
ALIVE = coloring('*', 'c')
POISON = coloring('x', 'r')
FOOD = coloring('o', 'g')

field = [[choice([DEAD, ALIVE]) for x in range(SIZE_X)] for y in range(SIZE_Y)]
'''field = [[DEAD for x in range(SIZE_X)] for y in range(SIZE_Y)]

for x in range(SIZE_X):
    for y in range(SIZE_Y):
        if x == 4 and y == 30 \
            or x == 5 and y == 30 \
            or x == 6 and y == 30 \
            or x == 6 and y == 29 \
            or x == 5 and y == 28:
                field[y][x] = ALIVE'''


def get_poison_and_food(field, prob):
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            field[y][x] = POISON if random() < prob and field[y][x] == DEAD else field[y][x]
            field[y][x] = FOOD if random() < prob and field[y][x] == DEAD else field[y][x]


def scanner(x, y):
    for dx, dy in (
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1)

    ):
        if x + dx == -1:
            scan_x = SIZE_X - x + dx
        elif x + dx == SIZE_X:
            scan_x = SIZE_X - (x + dx)
        else:
            scan_x = x + dx

        if y + dy == -1:
            scan_y = SIZE_Y - y + dy
        elif y + dy == SIZE_Y:
            scan_y = SIZE_Y - (y + dy)
        else:
            scan_y = y + dy
        yield scan_x, scan_y


def get_field(field):
    for y in range(SIZE_Y):
        print(''.join(field[y]))


def get_empty_field(field):
    return [[DEAD for x in range(SIZE_X)] for y in range(SIZE_Y)]


def is_alive(field, neighbor_x, neighbor_y):
    return 0 <= neighbor_x < SIZE_X \
           and 0 <= neighbor_y < SIZE_Y \
           and field[neighbor_y][neighbor_x] == ALIVE


def is_poison(field, neighbor_x, neighbor_y):
    return 0 <= neighbor_x < SIZE_X \
           and 0 <= neighbor_y < SIZE_Y \
           and field[neighbor_y][neighbor_x] == POISON


def is_food(field, neighbor_x, neighbor_y):
    return 0 <= neighbor_x < SIZE_X \
           and 0 <= neighbor_y < SIZE_Y \
           and field[neighbor_y][neighbor_x] == FOOD


generation = 0
while True:
    get_poison_and_food(field, .0001)
    print(f'Generation: {generation}')
    get_field(field)
    buffer = get_empty_field(field)

    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            cell = field[y][x]
            neighbors = 0

            for neighbor_x, neighbor_y in scanner(x, y):
                if is_food(field, neighbor_x, neighbor_y) and cell == ALIVE:
                    buffer[neighbor_y][neighbor_x] = ALIVE
                if is_poison(field, neighbor_x, neighbor_y) and cell == ALIVE:
                    cell = DEAD
                    buffer[neighbor_y][neighbor_x] = FOOD
                neighbors += 1 if is_alive(field, neighbor_x, neighbor_y) else 0

            if cell == DEAD:
                buffer[y][x] = ALIVE if neighbors == 3 else DEAD
            else:
                buffer[y][x] = ALIVE if neighbors in (2, 3) else DEAD

            if field[y][x] == POISON:
                buffer[y][x] = POISON if random() > .1 else DEAD
            if field[y][x] == FOOD:
                buffer[y][x] = FOOD if random() > .1 else DEAD

    if field == buffer:
        print('terminal state')
        break
    field = buffer
    generation += 1

    system('clear' if name != 'nt' else 'cls')
