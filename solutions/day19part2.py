from enum import Enum


class Stripes(Enum):
    WHITE = "w"
    BLUE = "u"
    BLACK = "b"
    GREEN = "g"
    RED = "r"


colour_dict = {
    Stripes.WHITE: 0,
    Stripes.BLUE: 1,
    Stripes.BLACK: 2,
    Stripes.GREEN: 3,
    Stripes.RED: 4,
}


checked_result = {}


def replace_all(input_in):
    copy = input_in
    for colour in colour_dict.keys():
        copy = copy.replace(colour.value, str(colour_dict[colour]))
    return [int(i) for i in list(copy)]


with open("../inputs/day19.txt") as f:
    lines = [line.strip() for line in f.readlines()]

components = [i.strip() for i in lines[0].split(",")]
components = [replace_all(i) for i in components]
to_make = lines[2:]
to_make = [replace_all(i) for i in to_make]


def possible_designs(list_in):
    res = 0, False
    if tuple(list_in) in checked_result.keys():
        return checked_result[tuple(list_in)]
    if not list_in:
        return 1, True
    for component in components:
        if len(list_in) < len(component):
            continue
        if list_in[:len(component)] == component:
            p = possible_designs(list_in[len(component):])
            if p[1]:
                res = (res[0] + p[0], True)
    checked_result[tuple(list_in)] = res
    return res


possible = 0
checked = 0
for item in to_make:
    possible += possible_designs(item)[0]
    checked += 1
    print(f"{checked} {possible}")


print(f"result = {possible}")
