with open("../inputs/day4.txt") as f:
    lines = f.readlines()
    lines = [i.strip() for i in lines]


def get_cross(row, column):
    return "".join([
        lines[row - 1][column - 1],
        lines[row - 1][column + 1],
        lines[row + 1][column + 1],
        lines[row + 1][column - 1],
    ])


count = 0
for i in range(1, len(lines) - 1):
    for j in range(1, len(lines[0]) - 1):
        if lines[i][j] == "A":
            try:
                cross = get_cross(i, j)
                if cross.lower() in [
                    "mmss",
                    "mssm",
                    "ssmm",
                    "smms",
                ]:
                    count += 1
            except IndexError:
                pass
print(count)
