with open("../inputs/day9.txt") as f:
    lines = [i.strip() for i in f.readlines()]


def to_expanded(str_in: str) -> list:
    l1 = []
    space = False
    count = 0
    for char in str_in:
        char_int = int(char)
        if not space:
            for i in range(char_int):
                l1.append(count)
            count += 1
        else:
            for i in range(char_int):
                l1.append(-1)
        space = not space
    return l1


def get_gaps(list_in: list) -> list[(int, int)]:
    res = []
    count = 0
    position = 0
    run = False
    for i in range(len(list_in)):
        if list_in[i] == -1:
            if not run:
                position = i
            run = True
            count += 1
        else:
            if run:
                res.append((position, count))
            run = False
            count = 0
    return res


def get_end_run(list_in: list) -> (int, int):
    end_value = list_in[-1]
    count = 0
    for i in range(len(list_in)):
        if list_in[-i - 1] == end_value:
            count += 1
        else:
            break
    return end_value, count


def get_new_position(options, target) -> int:
    possible_options = [option for option in options if option[1] >= target[1]]
    if possible_options:
        return possible_options[0][0]
    else:
        return -1


def splice(list_in: list, end, target_position) -> list:
    end_digit = end[0]
    end_length = end[1]
    res1 = list_in[:-end_length]
    for i in range(end_length):
        res1[i + target_position] = end_digit
    return res1


def compress(list_in: list) -> list:
    res = list_in
    extra = []
    for i in range(len(list_in)):
        if not res:
            break
        if res[-1] == -1:
            extra = [-1] + extra
            res.pop()
            continue
        g = (get_gaps(res))
        e = (get_end_run(res))
        t = (get_new_position(g, e))
        if t == -1:
            extra = res[-e[1]:] + extra
            res = res[:-e[1]]
        else:
            res = splice(res, e, t)
            for i in range(e[1]):
                extra.insert(0, -1)
        # print(f"{i}, {res + extra}")
    return res + extra


def get_checksum(list_in: list):
    return sum([i0 * i for i0, i in enumerate(list_in) if i != -1])


def solve(str_in, should_print=True, no_print=False):
    l2 = to_expanded(str_in)
    if should_print:
        print(f"{str_in} expanded: {l2}")
    l3 = compress(l2)
    if should_print:
        print(f"{str_in} compressed: {l3}")
    if not no_print:
        print(f"{str_in} checksum: {get_checksum(l3)}")
    return get_checksum(l3)


def listify(str_in):
    res = []
    for i in list(str_in):
        if i == ".":
            res.append(-1)
        else:
            res.append(int(i))
    return res


assert get_gaps([1, -1, -1, 1, -1, 1, -1, -1, -1, 1]) == [(1, 2), (4, 1), (6, 3)]
assert get_end_run([1, 1, 2, 3, 3, 3, 3, 3]) == (3, 5)
assert get_new_position([(0, 1), (2, 1), (5, 3), (6, 7)], (3, 2)) == 5
assert solve("1", no_print=True, should_print=False) == 0
assert to_expanded("2333133121414131402") == listify("00...111...2...333.44.5555.6666.777.888899")
# assert compress(to_expanded("1123431")) == [0, 3, 1, 1, -1, -1, -1, 2, 2, 2, 2, -1, -1, -1]


te = to_expanded("2333133121414131402")
print(te)
print(compress(te))
print(listify("00992111777.44.333....5555.6666.....8888"))

# assert compress(to_expanded("2333133121414131402")) == listify("00992111777.44.333....5555.6666.....8888")
assert solve("2333133121414131402") == 2858

print("SOLVING PROBLEM")
solve(lines[0], should_print=True)