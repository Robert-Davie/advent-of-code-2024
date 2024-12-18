GRID_HEIGHT = 71
GRID_WIDTH = 71
START = (0, 0)
END = (GRID_WIDTH - 1, GRID_HEIGHT - 1)


def get_adj_positions(position_in):
    p0 = position_in[0]
    p1 = position_in[1]
    possible = [
        (p0, p1 - 1),
        (p0 + 1, p1),
        (p0, p1 + 1),
        (p0 - 1, p1),
    ]
    return [i for i in possible if all([
        i[0] >= 0,
        i[1] >= 0,
        i[0] < GRID_WIDTH,
        i[1] < GRID_HEIGHT,
    ])]


with open("../inputs/day18.txt") as f:
    blocked_positions = [[int(j) for j in i.strip().split(",")] for i in f.readlines()]

blocked_positions = [tuple(i) for i in blocked_positions]
blocked_positions = tuple(blocked_positions)


def solve(number_of_objects):
    blocked_positions_copy = blocked_positions[:number_of_objects]
    distance_dict = {(i, j): -1 for i in range(GRID_WIDTH) for j in range(GRID_HEIGHT)
                     if (i, j) not in blocked_positions_copy}
    distance_dict[(0, 0)] = 0
    counter = 0
    updates = 1
    while distance_dict[END] == -1:
        if updates == 0:
            return False
        updates = 0
        counter += 1
        for key, value in distance_dict.items():
            if value == -1:
                for adjacent in get_adj_positions(key):
                    if adjacent not in distance_dict.keys():
                        continue
                    if distance_dict[adjacent] != -1:
                        distance_dict[key] = distance_dict[adjacent] + 1
                        updates += 1
                        break
    return True

# print("***GRID***")
#
# with open("../inputs/day18map.txt", "w") as f:
#     for j in range(GRID_HEIGHT):
#         # print(f"row = {j}")
#         for i in range(GRID_WIDTH):
#             try:
#                 if distance_dict[(i, j)] == -1:
#                     f.write(".")
#                 else:
#                     f.write("O")
#             except KeyError:
#                 f.write("#")
#         f.write("\n")


lower_bound = 1024
upper_bound = 3450
while upper_bound - lower_bound > 1:
    print(f"{upper_bound}, {lower_bound}")
    midpoint = (lower_bound + upper_bound) // 2
    if solve(midpoint):
        lower_bound = midpoint
    else:
        upper_bound = midpoint
# this returns the actual answer
print(blocked_positions[:upper_bound][-1])
