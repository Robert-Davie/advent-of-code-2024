import time

t0 = time.time()

from enum import Enum
from copy import deepcopy

with open("../inputs/day6.txt") as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]

GRID_HEIGHT = len(lines)
GRID_WIDTH = len(lines[0])


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def get_direction():
    full_string = "".join(lines)
    if "^" in full_string:
        return Direction.NORTH
    elif ">" in full_string:
        return Direction.EAST
    elif "v" in full_string:
        return Direction.SOUTH
    elif "<" in full_string:
        return Direction.WEST
    else:
        raise Exception("Guard not on grid")


def next_direction(direction):
    match direction:
        case Direction.NORTH:
            return Direction.EAST
        case Direction.EAST:
            return Direction.SOUTH
        case Direction.SOUTH:
            return Direction.WEST
        case Direction.WEST:
            return Direction.NORTH


def get_guard_location():
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if lines[i][j] in ["^", ">", "v", "<"]:
                return i, j


def get_obstacles():
    obstacles = list()
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if lines[i][j] == "#":
                obstacles.append((i, j))
    return obstacles


class Solver:
    def __init__(self):
        self.original_direction = get_direction()
        self.original_location = get_guard_location()
        self.original_obstacles = get_obstacles()
        self.current_direction = deepcopy(self.original_direction)
        self.current_location = deepcopy(self.original_location)
        self.current_obstacles = deepcopy(self.original_obstacles)
        self.visited_positions = []
        self.could_be_loop = True

    def filter_by_column(self, column):
        return [obstacle[0] for obstacle in self.current_obstacles if obstacle[1] == column]

    def filter_by_row(self, row):
        return [obstacle[1] for obstacle in self.current_obstacles if obstacle[0] == row]

    def go_to_next_stop(self):
        any_obstacles = []
        if self.current_direction == Direction.NORTH:
            any_obstacles = sorted([
                value for value in self.filter_by_column(self.current_location[1]) if value < self.current_location[0]
            ])
        elif self.current_direction == Direction.EAST:
            any_obstacles = sorted([
                value for value in self.filter_by_row(self.current_location[0]) if value > self.current_location[1]
            ])
        elif self.current_direction == Direction.SOUTH:
            any_obstacles = sorted([
                value for value in self.filter_by_column(self.current_location[1]) if value > self.current_location[0]
            ])
        if self.current_direction == Direction.WEST:
            any_obstacles = sorted([
                value for value in self.filter_by_row(self.current_location[0]) if value < self.current_location[1]
            ])

        if not any_obstacles:
            self.could_be_loop = False
            return
        else:
            match self.current_direction:
                case Direction.NORTH:
                    self.current_location = (any_obstacles[-1] + 1, self.current_location[1])
                    self.current_direction = Direction.EAST
                case Direction.EAST:
                    self.current_location = (self.current_location[0], any_obstacles[0] - 1)
                    self.current_direction = Direction.SOUTH
                case Direction.SOUTH:
                    self.current_location = (any_obstacles[0] - 1, self.current_location[1])
                    self.current_direction = Direction.WEST
                case Direction.WEST:
                    self.current_location = (self.current_location[0], any_obstacles[-1] + 1)
                    self.current_direction = Direction.NORTH

    def results_in_loop(self):
        self.could_be_loop = True
        self.visited_positions = []
        loop_result = None
        for iteration in range(10000):
            if not self.could_be_loop:
                loop_result = False
                break
            if (self.current_location, self.current_direction) in self.visited_positions:
                loop_result = True
                break
            else:
                self.visited_positions.append((self.current_location, self.current_direction))
            if iteration == 9998:
                raise Exception("too many iterations")
            self.go_to_next_stop()
        return loop_result

    def original_path(self):
        res = []
        self.current_location = self.original_location
        self.current_direction = self.original_direction
        while True:
            res.append(self.current_location)
            next_location = None
            match self.current_direction:
                case Direction.NORTH:
                    next_location = (self.current_location[0] - 1, self.current_location[1])
                case Direction.EAST:
                    next_location = (self.current_location[0], self.current_location[1] + 1)
                case Direction.SOUTH:
                    next_location = (self.current_location[0] + 1, self.current_location[1])
                case Direction.WEST:
                    next_location = (self.current_location[0], self.current_location[1] - 1)
            if next_location in self.original_obstacles:
                self.current_direction = next_direction(self.current_direction)
            else:
                self.current_location = next_location
            if any([
                self.current_location[0] == 0,
                self.current_location[1] == 0,
                self.current_location[0] == GRID_HEIGHT - 1,
                self.current_location[1] == GRID_WIDTH - 1,
            ]):
                res.append(self.current_location)
                break
        return list(set(res))

    def solve_problem(self):
        count = 0
        check_positions = self.original_path()
        for row0 in range(GRID_HEIGHT):
            for column0 in range(GRID_WIDTH):
                if lines[row0][column0] != "#" and (row0, column0) != self.original_location and (row0, column0) in check_positions:
                    self.current_location = deepcopy(self.original_location)
                    self.current_direction = self.original_direction
                    self.current_obstacles = self.original_obstacles + [(row0, column0)]
                    # print(row0, column0, end="")
                    if self.results_in_loop():
                        print(row0, column0)
                        # self.visited_positions_to_grid()
                        # print("loop")
                        # print(self.visited_positions)
                        count += 1
                    else:
                        pass
                        # print()
        print(count)

    def visited_positions_to_grid(self):
        for row0 in range(GRID_HEIGHT):
            for column0 in range(GRID_WIDTH):
                if (row0, column0) in self.original_obstacles:
                    print("#", end="")
                elif (row0, column0) in self.current_obstacles:
                    print("O", end="")
                elif (row0, column0) in [item[0] for item in self.visited_positions]:
                    print("+", end="")
                else:
                    print(".", end="")
            print()
        print()


s = Solver()
s.solve_problem()

t1 = time.time()
print(t1 - t0)
