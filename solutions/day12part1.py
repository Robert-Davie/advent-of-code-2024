from enum import Enum

with open("../inputs/day12.txt") as f:
    lines = [line.strip() for line in f.readlines()]

print(lines)
GRID_WIDTH = len(lines[0])
GRID_HEIGHT = len(lines)

# to_find = []
# for i in range(GRID_HEIGHT):
#     for j in range(GRID_WIDTH):
#         to_find.append((i, j))


def get_locations(letter):
    res = []
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if lines[i][j] == letter:
                res.append((i, j))
    return res


def get_perimeter(location_set_in):
    res = 0
    for location in location_set_in:
        res += 4
        l0 = location[0]
        l1 = location[1]
        if (l0 - 1, l1) in location_set_in:
            res -= 2
        if (l0, l1 - 1) in location_set_in:
            res -= 2
    return res
#
#
letters = list(set(char for char in "".join(lines)))
letters.sort()
# print(letters)
locations = [get_locations(letter) for letter in letters]
# regions = locations
# areas = {region: len(get_locations(region)) for region in regions}
# perimeters = {region: get_perimeter(region) for region in regions}
#
#
# print(locations)
# print(areas)
# print(perimeters)
#
# result = sum([areas[letter] * perimeters[letter] for letter in letters])
# print(f"result = {result}")


def is_adjacent(l1, l2):
    return l2 in get_adjacent_positions(l1)


def get_adjacent_positions(l1):
    return [
        (l1[0] - 1, l1[1]),
        (l1[0] + 1, l1[1]),
        (l1[0], l1[1] - 1),
        (l1[0], l1[1] + 1),
    ]


def get_regions(locations_in):
    locations_copy = locations_in
    res = []
    region = []

    while len(locations_copy) != 0:
        region.append(locations_copy.pop())
        has_update_occurred = True
        while has_update_occurred:
            new_points = []
            for region_point in region:
                new_points.extend(get_adjacent_positions(region_point))
            new_points = list(set(new_points))
            has_update_occurred = False
            for new_point in new_points:
                if new_point in locations_copy:
                    has_update_occurred = True
                    locations_copy.remove(new_point)
                    region.append(new_point)
        res.append(region)
        region = []
    return res

# print(locations)


def get_adjacent_with_diagonal_positions(point):
    p0 = point[0]
    p1 = point[1]
    return [
        (p0 - 1, p1 - 1),
        (p0 - 1, p1),
        (p0 - 1, p1 + 1),
        (p0, p1 - 1),
        (p0, p1 + 1),
        (p0 + 1, p1 - 1),
        (p0 + 1, p1),
        (p0 + 1, p1 + 1),
    ]


# def get_sides(region):
#     res = 0
#     all_points = []
#     for point in region:
#         all_points.extend(get_adjacent_with_diagonal_positions(point))
#     outer = [point for point in all_points if point not in region]
#     outer = set(outer)
#     for point in outer:
#         p1 = (point[0] - 1, point[1])
#         p2 = (point[0] + 1, point[1])
#         p3 = (point[0], point[1] - 1)
#         p4 = (point[0], point[1] + 1)
#         is_horizontal_edge = (p1 not in outer and p2 not in outer)
#         is_vertical_edge = (p3 not in outer and p4 not in outer)
#
#         if not (is_horizontal_edge or is_vertical_edge):
#             res += 1
#     return res


# def get_leftmost_point(region_in):
#     min_row = min([i[0] for i in region_in])
#     min_col = sorted([point[1] for point in region_in if point[0] == min_row])[0]
#     return min_row, min_col


# class Direction(Enum):
#     NORTH = 0,
#     EAST = 1,
#     SOUTH = 2,
#     WEST = 3,


# def get_next_point(point, direction):
#     p0 = point[0]
#     p1 = point[1]
#     match direction:
#         case Direction.NORTH:
#             return p0 - 1, p1
#         case Direction.EAST:
#             return p0, p1 + 1
#         case Direction.SOUTH:
#             return p0 + 1, p1
#         case Direction.WEST:
#             return p0, p1 - 1


# def get_container(region_in):
#     end = get_leftmost_point(region_in)
#     candidates = []
#     for point in region_in:
#         if [i for i in get_adjacent_positions(point) if i not in region_in]:
#             candidates.append(point)


def get_sides():
    for point in region:
        pass


assert get_sides([(0, 0)]) == 4
assert get_sides([(0, 0), (1, 0), (1, 1), (2, 1)]) == 8
assert get_sides([(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]) == 8
assert not is_adjacent((1, 0), (0, 1))
assert is_adjacent((1, 1), (1, 2))
print(get_regions([(0, 0), (0, 1), (1, 1), (1, 2), (3, 3)]))


regions = []
for location_group in locations:
    regions.extend(get_regions(location_group))
print(regions)

count = 0
for region in regions:
    area = len(region)
    sides = get_sides(region)
    print(region[0], area, sides)
    count += area * sides
print(count)