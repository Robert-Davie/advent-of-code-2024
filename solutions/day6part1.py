from enum import Enum

with open("../inputs/day6.txt") as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]

GRID_HEIGHT = len(lines)
GRID_WIDTH = len(lines[0])


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def get_direction():
    full_string = "".join(lines)
    if "^" in full_string:
        return Direction.NORTH
    elif ">" in full_string:
        return Direction.EAST
    elif "v" in full_string:
        return Direction.SOUTH
    elif "<" in full_string:
        return Direction.WEST
    else:
        raise Exception("Guard not on grid")


def get_guard_location():
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if lines[i][j] in ["^", ">", "v", "<"]:
                return i, j


def get_visited_squares():
    res = 0
    for line in lines:
        res += line.count("X")
    return res


def rotate_guard():
    l0, l1 = get_guard_location()
    guard_direction = get_direction()
    match guard_direction:
        case Direction.NORTH:
            lines[l0] = lines[l0].replace("^", ">")
        case Direction.EAST:
            lines[l0] = lines[l0].replace(">", "v")
        case Direction.SOUTH:
            lines[l0] = lines[l0].replace("v", "<")
        case Direction.WEST:
            lines[l0] = lines[l0].replace("<", "^")


def is_end_condition_met():
    l0, l1 = get_guard_location()
    guard_direction = get_direction()
    match guard_direction:
        case Direction.NORTH:
            return l0 == 0
        case Direction.EAST:
            return l1 == GRID_WIDTH - 1
        case Direction.SOUTH:
            return l0 == GRID_HEIGHT - 1
        case Direction.WEST:
            return l1 == 0


def guard_next_location_if_forward():
    l0, l1 = get_guard_location()
    guard_direction = get_direction()
    match guard_direction:
        case Direction.NORTH:
            return l0 - 1, l1
        case Direction.EAST:
            return l0, l1 + 1
        case Direction.SOUTH:
            return l0 + 1, l1
        case Direction.WEST:
            return l0, l1 - 1


def update_lines(char, row, column):
    line = list(lines[row])
    line[column] = char
    lines[row] = "".join(line)


guard_direction_dict = {
    Direction.NORTH: "^",
    Direction.EAST: ">",
    Direction.SOUTH: "v",
    Direction.WEST: "<",
}


def get_guard_character():
    return guard_direction_dict[get_direction()]


def guard_next_move():
    l0, l1 = get_guard_location()
    m0, m1 = guard_next_location_if_forward()
    if lines[m0][m1] == "#":
        rotate_guard()
    else:
        update_lines(get_guard_character(), m0, m1)
        update_lines("X", l0, l1)


while not is_end_condition_met():
    guard_next_move()
f0, f1 = get_guard_location()
update_lines("X", f0, f1)

for line in lines:
    print(line)
print(get_visited_squares())

