import re

with open("../inputs/day13.txt") as f:
    lines = [line.strip() for line in f.readlines()]
    lines = [line for line in lines if line != ""]

WEIGHTING_A = 3
WEIGHTING_B = 1
ADD_TEN_TRILLION = True

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
    if ADD_TEN_TRILLION:
        total = [total_part + 10_000_000_000_000 for total_part in total]
    equations.append((a, b, total))


print(equations)


def get_a(equation_in):
    v1 = equation_in[0][0]
    v2 = equation_in[0][1]
    v3 = equation_in[1][0]
    v4 = equation_in[1][1]
    req_x = equation_in[2][0]
    req_y = equation_in[2][1]

    numerator = (v4 * req_x) - (v3 * req_y)
    denominator = (v1 * v4) - (v2 * v3)
    if denominator == 0:
        return -1
    return numerator // denominator


def are_a_b_co_linear(t1, t2):
    return round(t1[0] / t2[0], 5) == round(t1[1] / t2[1], 5)


def check_result(a1, b1, e1):
    a_part = e1[0]
    b_part = e1[1]
    t_part = e1[2]
    assert a_part[0] * a1 + b_part[0] * b1 == t_part[0]
    assert a_part[1] * a1 + b_part[1] * b1 == t_part[1]


def get_cost(equation_in):
    a = equation_in[0]
    b = equation_in[1]
    t = equation_in[2]

    a_req = get_a(equation_in)
    if a_req < 0:
        if are_a_b_co_linear(a, b):
            raise Exception("unimplemented A & B co-linear")
        return -1
    try:
        b_req = (t[0] - a[0] * a_req) // b[0]
    except ZeroDivisionError:
        return a_req * WEIGHTING_A
    if b_req < 0:
        return -1
    print(a_req, b_req)
    try:
        check_result(a_req, b_req, equation_in)
    except AssertionError:
        print(f"result is not valid")
        return -1
    return a_req * WEIGHTING_A + b_req * WEIGHTING_B


assert get_cost([[30, 20], [1, 2], [10, 20]]) == 10
assert get_cost([[10, 15], [1, 3], [11, 18]]) == 4
assert get_cost(([94, 34], [22, 67], [8400, 5400])) == 280
assert get_cost([[30, 20], [0, 1], [30, 20]]) == 3
assert get_cost([[30, 20], [1, 0], [30, 20]]) == 3
assert get_cost([[0, 1], [30, 20], [30, 20]]) == 1

print("*** FINISHED ASSERTS ***\n\n")

total = 0
for equation in equations:
    cost = get_cost(equation)
    print(cost)
    if cost >= 0:
        total += cost

print(f"PART 2 total = {total}")
print(f"ADD TEN TRILLION WAS {'NOT ' if not ADD_TEN_TRILLION else ''}USED")
