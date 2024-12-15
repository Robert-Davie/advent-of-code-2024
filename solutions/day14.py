import re


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


def run_simulation(time):
    res = []
    for guard in guards:
        guard_x = (guard[0][0] + time * guard[1][0]) % GRID_WIDTH
        guard_y = (guard[0][1] + time * guard[1][1]) % GRID_HEIGHT
        guard_final = (guard_x, guard_y)
        res.append(guard_final)
    print(get_safety_factor(res))


def get_safety_factor(list_in):
    midpoint_x = GRID_WIDTH // 2
    midpoint_y = GRID_HEIGHT // 2
    quad_counts = {
        (-1, -1): 0,
        (-1, 1): 0,
        (1, -1): 0,
        (1, 1): 0,
    }
    for point in list_in:
        point_x = point[0]
        point_y = point[1]

        if point_x < midpoint_x:
            if point_y < midpoint_y:
                quad_counts[(-1, -1)] += 1
            elif point_y > midpoint_y:
                quad_counts[(-1, 1)] += 1
        elif point_x > midpoint_x:
            if point_y < midpoint_y:
                quad_counts[(1, -1)] += 1
            elif point_y > midpoint_y:
                quad_counts[(1, 1)] += 1
    q = quad_counts
    return q[(-1, -1)] * q[(-1, 1)] * q[(1, -1)] * q[(1, 1)]


print(guards)
run_simulation(100)
