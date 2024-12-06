import re


def make_line_string(lines_in):
    res2 = ""
    joined_string = "".join(lines_in)
    s1 = re.finditer("don't\(\)",joined_string)
    s2 = re.finditer("do\(\)",joined_string)
    stop = [i.start() for i in s1]
    start = [i.start() for i in s2]

    do = True
    for char0 in range(len(joined_string)):
        if char0 in stop:
            do = False
        elif char0 in start:
            do = True
        if do:
            res2 += joined_string[char0]

    return res2


def count_matches(line_in):
    count = 0
    for match in re.findall("mul\((\d+),(\d+)\)", line_in):
        count += int(match[0]) * int(match[1])
    return count


with open("../inputs/day3.txt") as f:
    lines = f.readlines()

line = make_line_string(lines)
res = count_matches(line)

print(res)