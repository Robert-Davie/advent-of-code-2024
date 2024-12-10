# the changes to solve part 2 are on lines 51 & 57

with open("../inputs/day10.txt") as f:
    lines = [[int(j) for j in list(i.strip())] for i in f.readlines()]


GRID_HEIGHT = len(lines)
GRID_WIDTH = len(lines[0])


def get_by_digit(number: int) -> list[(int, int)]:
    res = []
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == number:
                res.append((i, j))
    return res


def is_valid_position(position: (int, int)) -> bool:
    return all([
        position[0] >= 0,
        position[1] >= 0,
        position[0] < GRID_HEIGHT,
        position[1] < GRID_WIDTH,
    ])


def get_adjacent(position: (int, int)) -> list[(int, int)]:
    res = [
        (position[0] - 1, position[1]),
        (position[0] + 1, position[1]),
        (position[0], position[1] - 1),
        (position[0], position[1] + 1),
    ]
    return [i for i in res if is_valid_position(i)]


def value_at_position(tuple_in: (int, int)) -> int:
    return lines[tuple_in[0]][tuple_in[1]]


def possible_end_points(start: (int, int)) -> list[int, int]:
    if value_at_position(start) != 0:
        raise ValueError("start position must be 0")
    current_choices = [[start]]
    next_choices = []

    for k in range(1, 10):
        for choice in current_choices:
            res = [choice + [i] for i in get_adjacent(choice[-1]) if value_at_position(i) == k]
            next_choices.extend(res)
        current_choices = next_choices
        next_choices = []
        # print(f"{k} {current_choices}")

    return current_choices


zeroes = get_by_digit(0)
nines = get_by_digit(9)

count = 0
for zero in zeroes:
    count += len(possible_end_points(zero))
print(count)
