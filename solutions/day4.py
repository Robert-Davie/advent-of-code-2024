import numpy as np
import re


def get_count(string):
    matches1 = re.findall("XMAS", string)
    matches2 = re.findall("XMAS", string[::-1])
    return len(matches1) + len(matches2)


with open("../inputs/day4.txt") as f:
    lines = f.readlines()
    lines = [i.strip() for i in lines]

data = np.array([list(i) for i in lines])

total = 0

for line in lines:
    total += get_count(line)
for i in range(len(lines[0])):
    total += get_count("".join(data[:, i]))
for i in range(len(lines[0]) + len(lines) - 1):
    total += get_count("".join(np.diag(data, i - len(lines) + 1)))
data2 = np.flip(data, axis=1)
for i in range(len(lines[0]) + len(lines) - 1):
    total += get_count("".join(np.diag(data2, i - len(lines) + 1)))

print(total)
