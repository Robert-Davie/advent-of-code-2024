# the change made to solve part 2 is in the get_spots function


with open("../inputs/day8.txt") as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]


COLUMNS = len(lines[0])
ROWS = len(lines)

ant_dict = dict()


def get_antennae():
    for i in range(ROWS):
        for j in range(COLUMNS):
            value = lines[i][j]
            if value != ".":
                ant_dict[(i, j)] = value


get_antennae()

new_dict = {i: [] for i in set(ant_dict.values())}
for key, value in ant_dict.items():
    new_dict[value].append(key)
print(new_dict)


def get_spots(tuple1, tuple2):
    a0, a1 = tuple1
    b0, b1 = tuple2
    d0 = b0 - a0
    d1 = b1 - a1
    max_of_rows_and_columns = max(ROWS, COLUMNS)
    return [(a0 + i * d0, a1 + i * d1) for i in range(-max_of_rows_and_columns, max_of_rows_and_columns)]


spots = []
for _, value in new_dict.items():
    for i in value:
        for j in value:
            if i == j:
                continue
            spots = spots + get_spots(i, j)
s = [i for i in set(spots) if 0 <= i[0] < ROWS and 0 <= i[1] < COLUMNS]
print(s)
print(len(s))

for i in range(ROWS):
    for j in range(COLUMNS):
        if (i, j) in s:
            print("#", end="")
        else:
            print(".", end="")
    print()


print(f"answer = {len(s)}")