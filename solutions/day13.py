import re

with open("../inputs/day13.txt") as f:
    lines = [line.strip() for line in f.readlines()]
    lines = [line for line in lines if line != ""]

WEIGHTING_A = 3
WEIGHTING_B = 1

machines = []
for i in range(len(lines) // 3):
    machines.append([lines[i * 3], lines[i * 3 + 1], lines[i * 3 + 2]])

equations = []
for machine in machines:
    a = re.findall("([+-]\d+)", machine[0])
    a = [int(a_part) for a_part in a]
    b = re.findall("([+-]\d+)", machine[1])
    b = [int(b_part) for b_part in b]
    total = re.findall("(\d+)", machine[2])
    total = [int(total_part) for total_part in total]
    equations.append((a, b, total))


def get_costs(equation_in):
    this_costs = []
    a = equation_in[0]
    b = equation_in[1]
    t = equation_in[2]
    for i in range(101):
        xreq = t[0] - a[0] * i
        yreq = t[1] - a[1] * i
        if xreq % b[0] == 0 and yreq % b[1] == 0:
            if xreq // b[0] == yreq // b[1]:
                this_costs.append(i * WEIGHTING_A + (xreq // b[0]) * WEIGHTING_B)
    return this_costs


assert get_costs([[30, 20], [1, 2], [10, 20]]) == [10]
assert get_costs([[10, 15], [1, 3], [11, 18]]) == [4]
assert get_costs(([94, 34], [22, 67], [8400, 5400])) == [280]

total = 0
for equation in equations:
    print(equation, total)
    costs = get_costs(equation)
    if costs:
        total += min(costs)

print(machines)
print(equations)
print(total)