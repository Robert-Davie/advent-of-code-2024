with open("../inputs/day11.txt") as f:
    lines = [i.strip() for i in f.readlines()]
    line = lines[0]
    line = [int(i) for i in line.split()]


d2 = {i: line.count(i) for i in set(line)}


def get_stones(stone_in: int):
    if stone_in == 0:
        return [1]
    elif len(str(stone_in)) % 2 == 0:
        s = str(stone_in)
        m = len(s) // 2
        return [int(s[:m]), int(s[m:])]
    else:
        return [stone_in * 2024]


next_stones = dict()
current_stones = d2
for k in range(75):
    print(k)
    for stone_value, number in current_stones.items():
        g = get_stones(stone_value)
        for next_stone in g:
            if next_stone in next_stones:
                next_stones[next_stone] += number
            else:
                next_stones[next_stone] = number

    current_stones = next_stones
    next_stones = dict()


def get_length(dict_in: dict):
    return sum(dict_in.values())


# assert get_stones(0) == [1]
# assert get_stones(1) == [2024]
# assert get_stones(2) == [4048]
# assert get_stones(2024) == [20, 24]
# assert get_stones(17) == [1, 7]
# print("ASSERTS PASSED")

print(get_length(current_stones))