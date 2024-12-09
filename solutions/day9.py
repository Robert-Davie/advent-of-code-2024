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


def compress(list_in: list) -> list:
    to_check = len(list_in)
    included = len([i for i in list_in if i != -1])
    res_list = []
    count = 0
    end_of_list = -1
    while True:
        if count >= included:
            break
        if list_in[count] == -1:
            while list_in[end_of_list] == -1:
                end_of_list -= 1
                to_check -= 1
            res_list.append(list_in[end_of_list])
            end_of_list -= 1
            to_check -= 1
        else:
            res_list.append(list_in[count])
            pass
        count += 1
    return res_list


def get_checksum(list_in: list):
    return sum([i0 * i for i0, i in enumerate(list_in)])


print(lines[0])
l2 = to_expanded(lines[0])
print(l2)
l3 = compress(l2)
print(l3)
print(get_checksum(l3))
