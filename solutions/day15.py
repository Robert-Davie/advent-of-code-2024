from enum import Enum


class CellType(Enum):
    WALL = "#"
    OBSTACLE = "O"
    GUARD = "@"
    EMPTY = "."


with open("../inputs/day15.txt") as f:
    lines = [i.strip() for i in f.readlines()]

grid = [list(i) for i in lines if i and i[0] == "#"]
instructions = [i for i in lines if i and i[0] != "#"]
instructions = "".join(instructions)

instruction_dict = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}

instructions = [instruction_dict[i] for i in instructions]

GRID_WIDTH = len(lines[0])
GRID_HEIGHT = len(grid)


def get_guard_position():
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if grid[i][j] == CellType.GUARD.value:
                return j, i


def get_all_matches(match):
    res = []
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if grid[i][j] == match.value:
                res.append((j, i))
    return res


guard_position = get_guard_position()
wall_positions = get_all_matches(CellType.WALL)
obstacle_positions = get_all_matches(CellType.OBSTACLE)


def get_gps_sum():
    return sum([i[1] * 100 + i[0] for i in obstacle_positions])


def get_next_cell_type(start, movement):
    final = add_movement(start, movement)
    return get_cell_type(final)


def get_cell_type(cell):
    if cell in obstacle_positions:
        return CellType.OBSTACLE
    elif cell in wall_positions:
        return CellType.WALL
    elif cell == guard_position:
        return CellType.GUARD
    else:
        return CellType.EMPTY


def add_movement(start, movement):
    s0, s1 = start
    m0, m1 = movement
    final = s0 + m0, s1 + m1
    return final


def find_run_end(start, movement):
    curr_pos = start
    while get_next_cell_type(curr_pos, movement) == CellType.OBSTACLE:
        curr_pos = add_movement(curr_pos, movement)
    return add_movement(curr_pos, movement)


def attempt_move_guard(movement):
    global guard_position
    guard_attempt_location = add_movement(guard_position, movement)
    run_end = find_run_end(guard_position, movement)
    if get_cell_type(run_end) == CellType.EMPTY:
        obstacle_positions.append(run_end)
        obstacle_positions.remove(guard_attempt_location)
        guard_position = guard_attempt_location


def print_grid():
    for j in range(GRID_HEIGHT):
        for i in range(GRID_WIDTH):
            if (i, j) in obstacle_positions:
                print("O", end="")
            elif (i, j) in wall_positions:
                print("#", end="")
            elif (i, j) == guard_position:
                print("@", end="")
            else:
                print(".", end="")
        print()


assert add_movement((1, 3), (0, 1)) == (1, 4)


for instruction in instructions:
    attempt_move_guard(instruction)

# print(grid)
# print(guard_position)
# print(obstacle_positions)

OK_GREEN = '\033[92m'
END_C = '\033[0m'
print_grid()
print(OK_GREEN + f"FINAL RESULT = {get_gps_sum()}" + END_C)
