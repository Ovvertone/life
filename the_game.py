from random import choice, random
from os import system, name

from colorama import Fore, Style
import matplotlib.pyplot as plt
from numpy import round


def coloring(text: str, color: str) -> str:
    colors = {'r': Fore.RED, 'g': Fore.GREEN, 'b': Fore.BLUE, 'c': Fore.LIGHTCYAN_EX, 'w': Fore.WHITE}
    try:
        return colors[color] + text + Style.RESET_ALL
    except KeyError:
        return text


SIZE_X = 190
SIZE_Y = 50
DEAD = ' '
ALIVE = coloring('*', 'c')
POISON = coloring('x', 'r')
FOOD = coloring('o', 'g')

field = [[choice([ALIVE, DEAD]) for x in range(SIZE_X)] for y in range(SIZE_Y)]


def get_poison_and_food(field: list, prob: float) -> None:
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            field[y][x] = POISON if random() < prob and field[y][x] == DEAD else field[y][x]
            field[y][x] = FOOD if random() < prob and field[y][x] == DEAD else field[y][x]


def scanner(x: int, y: int) -> (int, int):
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


def get_field(field: list) -> None:
    for y in range(SIZE_Y):
        print(''.join(field[y]))


def get_empty_field(field: list) -> list:
    return [[DEAD for x in range(SIZE_X)] for y in range(SIZE_Y)]


def check_cell(field: list, neighbor_x: int, neighbor_y: int, cell_type: str) -> bool:
    cell_types = {'alive': ALIVE, 'poison': POISON, 'food': FOOD}
    return 0 <= neighbor_x < SIZE_X \
           and 0 <= neighbor_y < SIZE_Y \
           and field[neighbor_y][neighbor_x] == cell_types[cell_type]


alive_list, generation_list, food_list, poison_list = [], [], [], []
generation = 1
while True:
    alive_count, food_count, poison_count = 0, 0, 0
    print(f'Generation: {generation}')
    get_poison_and_food(field, .0001)
    get_field(field)
    buffer = get_empty_field(field)

    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            cell = field[y][x]
            alive_count += 1 if cell == ALIVE else 0
            food_count += 1 if cell == FOOD else 0
            poison_count += 1 if cell == POISON else 0
            neighbors = 0

            for neighbor_x, neighbor_y in scanner(x, y):
                if check_cell(field, neighbor_x, neighbor_y, 'food') and cell == ALIVE:
                    buffer[neighbor_y][neighbor_x] = ALIVE
                if check_cell(field, neighbor_x, neighbor_y, 'poison') and cell == ALIVE:
                    cell = DEAD
                    buffer[neighbor_y][neighbor_x] = FOOD
                neighbors += 1 if check_cell(field, neighbor_x, neighbor_y, 'alive') else 0

            if cell == DEAD:
                buffer[y][x] = ALIVE if neighbors == 3 else DEAD
            else:
                buffer[y][x] = ALIVE if neighbors in (2, 3) else DEAD

            if field[y][x] == POISON:
                buffer[y][x] = POISON if random() > .05 else DEAD
            if field[y][x] == FOOD:
                buffer[y][x] = FOOD if random() > .05 else DEAD

    if field == buffer or generation == 500:
        print('terminal state')
        break
    field = buffer

    generation_list.append(generation)
    alive_list.append(alive_count)
    food_list.append(food_count)
    poison_list.append(poison_count)
    generation += 1

    system('clear' if name != 'nt' else 'cls')

fig, ax = plt.subplots()
plt.title('Diagram of cells count')
ax.plot(generation_list, [round((i / (SIZE_X * SIZE_Y)) * 100, 2) for i in alive_list], 'b', label='Alive')
ax.plot(generation_list, [round((i / (SIZE_X * SIZE_Y)) * 100, 2) for i in food_list], 'g', label='Food')
ax.plot(generation_list, [round((i / (SIZE_X * SIZE_Y)) * 100, 2) for i in poison_list], 'r', label='Poison')
ax.legend()
plt.axis([1, 500, 0, 100])
ax.set_xlabel('Generation')
ax.set_ylabel('Count of alive cells, food cells and poison cells (%)')
ax.grid()
fig.set_figwidth(18)
fig.set_figheight(9)
plt.show()
