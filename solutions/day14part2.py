import re
from collections import Counter


with open("../inputs/day14.txt") as f:
    lines = [line.strip() for line in f.readlines()]


GRID_HEIGHT = 103
GRID_WIDTH = 101



guards = []
print(lines)
for line in lines:
    r = re.findall("([-]?\d+),([-]?\d+)", line)
    values = (
        (
            int(r[0][0]),
            int(r[0][1])
        ), (
            int(r[1][0]),
            int(r[1][1])
        )
    )
    guards.append(values)


def run_simulation(time, print_this=False):
    res = []
    x_list = []
    y_list = []
    for guard in guards:
        guard_x = (guard[0][0] + time * guard[1][0]) % GRID_WIDTH
        guard_y = (guard[0][1] + time * guard[1][1]) % GRID_HEIGHT
        guard_final = (guard_x, guard_y)
        res.append(guard_final)
        x_list.append(guard_x)
        y_list.append(guard_y)
    top_x = Counter(x_list).most_common(1)[0][1]
    top_y = Counter(y_list).most_common(1)[0][1]
    if print_this:
        print_image(res)
    return top_x, top_y


def print_image(res_in):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if (i, j) in res_in:
                print("*", end="")
            else:
                print(".", end="")
        print()


# print(guards)
for i in range(100000):
    x, y = run_simulation(i)
    if x > 25 and y > 25:
        print(f"TIME {i}: {x} {y}")
