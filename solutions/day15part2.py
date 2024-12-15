from enum import Enum


class CellType(Enum):
    WALL = "#"
    OBSTACLE = "O"
    OBSTACLE_LEFT = "["
    OBSTACLE_RIGHT = "]"
    GUARD = "@"
    EMPTY = "."


class Movement(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


movement_dict = {
    (0, -1): Movement.UP,
    (1, 0): Movement.RIGHT,
    (0, 1): Movement.DOWN,
    (-1, 0): Movement.LEFT,
}


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

ORIGINAL_GRID_WIDTH = len(lines[0])
ORIGINAL_GRID_HEIGHT = len(grid)
GRID_WIDTH = ORIGINAL_GRID_WIDTH * 2
GRID_HEIGHT = ORIGINAL_GRID_HEIGHT


def get_guard_position():
    for i in range(ORIGINAL_GRID_HEIGHT):
        for j in range(ORIGINAL_GRID_WIDTH):
            if grid[i][j] == CellType.GUARD.value:
                return j * 2, i


def get_obstacles(obstacle_type):
    res = []
    for i in range(ORIGINAL_GRID_HEIGHT):
        for j in range(ORIGINAL_GRID_WIDTH):
            if grid[i][j] == CellType.OBSTACLE.value:
                extra = 0 if obstacle_type == CellType.OBSTACLE_LEFT else 1
                res.append((j * 2 + extra, i))
    return res


def get_walls():
    res = []
    for i in range(ORIGINAL_GRID_HEIGHT):
        for j in range(ORIGINAL_GRID_WIDTH):
            if grid[i][j] == CellType.WALL.value:
                res.append((j * 2, i))
                res.append((j * 2 + 1, i))
    return res


guard_position = get_guard_position()
wall_positions = get_walls()
obstacle_left_positions = get_obstacles(CellType.OBSTACLE_LEFT)
obstacle_right_positions = get_obstacles(CellType.OBSTACLE_RIGHT)


def get_gps_sum():
    return sum([i[1] * 100 + i[0] for i in obstacle_left_positions])


def get_next_cell_type(start, movement):
    final = add_movement(start, movement)
    return get_cell_type(final)


def get_cell_type(cell):
    if cell in obstacle_left_positions:
        return CellType.OBSTACLE_LEFT
    elif cell in obstacle_right_positions:
        return CellType.OBSTACLE_RIGHT
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


def get_run_vertical(start, movement):
    curr_pos = [start]
    all_empty = False
    res = []
    while not all_empty:
        all_empty = True
        temp_pos = []
        for position in curr_pos:
            next_pos = add_movement(position, movement)
            next_pos_type = get_cell_type(next_pos)
            if next_pos_type == CellType.WALL:
                return []
            elif next_pos_type == CellType.OBSTACLE_LEFT:
                all_empty = False
                temp_pos.append(next_pos)
                temp_pos.append(add_movement(next_pos, Movement.RIGHT.value))
            elif next_pos_type == CellType.OBSTACLE_RIGHT:
                all_empty = False
                temp_pos.append(next_pos)
                temp_pos.append((add_movement(next_pos, Movement.LEFT.value)))
        curr_pos = temp_pos
        res.extend(temp_pos)
    return list(set(res))


def find_run_end_horizontal(start, movement):
    assert movement[1] == 0
    curr_pos = start
    while get_next_cell_type(curr_pos, movement) in (CellType.OBSTACLE_LEFT, CellType.OBSTACLE_RIGHT):
        curr_pos = add_movement(curr_pos, movement)
    return add_movement(curr_pos, movement)


def get_obstacles_in_run_horizontal(start, movement):
    assert movement[1] == 0
    curr_pos = start
    res = []
    while get_next_cell_type(curr_pos, movement) in (CellType.OBSTACLE_LEFT, CellType.OBSTACLE_RIGHT):
        curr_pos = add_movement(curr_pos, movement)
        res.append(curr_pos)
    return res


def attempt_move_guard_horizontal(movement):
    global guard_position
    movement_direction = movement_dict[movement]
    guard_attempt_location = add_movement(guard_position, movement)
    run_end = find_run_end_horizontal(guard_position, movement)
    run = get_obstacles_in_run_horizontal(guard_position, movement)
    if get_cell_type(run_end) == CellType.EMPTY:
        if movement_direction == Movement.RIGHT:
            obstacle_right_positions.append(run_end)
            for position in run:
                if position in obstacle_right_positions:
                    obstacle_right_positions.remove(position)
                    obstacle_left_positions.append(position)
                else:
                    obstacle_left_positions.remove(position)
                    obstacle_right_positions.append(position)
            obstacle_right_positions.remove(guard_attempt_location)
        else:
            obstacle_left_positions.append(run_end)
            for position in run:
                if position in obstacle_right_positions:
                    obstacle_right_positions.remove(position)
                    obstacle_left_positions.append(position)
                else:
                    obstacle_left_positions.remove(position)
                    obstacle_right_positions.append(position)
            obstacle_left_positions.remove(guard_attempt_location)
        guard_position = guard_attempt_location


def attempt_move_guard_vertical(movement):
    global guard_position
    run = get_run_vertical(guard_position, movement)
    to_add = []
    for part in run:
        this_type = get_cell_type(part)
        to_add.append((add_movement(part, movement), this_type))
        if this_type == CellType.OBSTACLE_LEFT:
            obstacle_left_positions.remove(part)
        else:
            obstacle_right_positions.remove(part)
    for item in to_add:
        position, item_type = item
        if item_type == CellType.OBSTACLE_LEFT:
            obstacle_left_positions.append(position)
        else:
            obstacle_right_positions.append(position)
    if run:
        guard_position = add_movement(guard_position, movement)


def attempt_move_guard(movement):
    global guard_position
    attempt_position = add_movement(guard_position, movement)
    if get_cell_type(attempt_position) == CellType.EMPTY:
        guard_position = attempt_position
    elif movement[1] == 0:
        attempt_move_guard_horizontal(movement)
    else:
        attempt_move_guard_vertical(movement)


def print_grid():
    print(" ", end="")
    for i in range(GRID_WIDTH):
        print(i % 10, end="")
    print()
    for j in range(GRID_HEIGHT):
        print(j % 10, end="")
        for i in range(GRID_WIDTH):
            if (i, j) in obstacle_left_positions:
                print("[", end="")
            elif (i, j) in obstacle_right_positions:
                print("]", end="")
            elif (i, j) in wall_positions:
                print("#", end="")
            elif (i, j) == guard_position:
                print("@", end="")
            else:
                print(".", end="")
        print()


def force_move_guard(new_position):
    global guard_position
    if all([
        new_position not in obstacle_left_positions,
        new_position not in obstacle_right_positions,
        new_position not in wall_positions,
    ]):
        guard_position = new_position
    else:
        raise Warning(f"Guard cannot move to position {new_position}")

# assert add_movement((1, 3), (0, 1)) == (1, 4)


for instruction in instructions:
    # print_grid()
    attempt_move_guard(instruction)

# print(grid)
# print(guard_position)
# print(obstacle_positions)
attempt_move_guard(Movement.LEFT.value)
print(get_run_vertical((6, 5), Movement.UP.value))

OK_GREEN = '\033[92m'
END_C = '\033[0m'
print_grid()
print(OK_GREEN + f"FINAL RESULT = {get_gps_sum()}" + END_C)
