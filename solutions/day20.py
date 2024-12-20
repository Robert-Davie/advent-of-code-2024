from enum import Enum


class Movement(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


class CellType(Enum):
    WALL = "#"
    EMPTY = "."
    START = "S"
    END = "E"

    
def manhattan_distance(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])


def get_adj_positions(position_in):
    p0 = position_in[0]
    p1 = position_in[1]
    res = [
        (p0, p1 - 1),
        (p0 + 1, p1),
        (p0, p1 + 1),
        (p0 - 1, p1),
    ]
    return [i for i in res if 0 <= i[0] < GRID_WIDTH and 0 <= i[1] < GRID_HEIGHT]


with open("../inputs/day20.txt") as f:
    grid = [line.strip() for line in f.readlines()]


# print(grid)
GRID_HEIGHT = len(grid)
GRID_WIDTH = len(grid[0])


walls = []
empties = []
start = (-1, -1)
end = (-1, -1)


for j in range(GRID_HEIGHT):
    for i in range(GRID_WIDTH):
        cell = grid[j][i]
        if cell == CellType.START.value:
            start = (i, j)
        if cell == CellType.END.value:
            end = (i, j)
        if cell == CellType.WALL.value:
            walls.append((i, j))
        else:
            empties.append((i, j))


def get_next_cell(cell_in, prev_cell_in):
    for neighbour_cell in get_adj_positions(cell_in):
        if neighbour_cell not in walls and neighbour_cell != prev_cell_in:
            return neighbour_cell
    return None


# get path
path = []
current_cell = start
previous_cell = start
end_done = False
while not end_done:
    if current_cell == end:
        end_done = True
    path.append(current_cell)
    temp = get_next_cell(current_cell, previous_cell)
    previous_cell = current_cell
    current_cell = temp

path_positions = {point: p0 for p0, point in enumerate(path)}
# print(path_positions)

cheats = []
for wall in walls:
    orders = [path_positions[i] for i in get_adj_positions(wall) if i not in walls]
    try:
        cheats.append(max(orders) - min(orders))
    except ValueError:
        pass

cheats = [i - 2 for i in cheats if i >= 2]

print(len([i for i in cheats if i >= 100]))