with open("../inputs/day7.txt") as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]

cleaned = []
for line in lines:
    part1, part2 = line.split(":")
    numbers = [int(number.strip()) for number in part2.split(" ") if number != ""]
    part1 = int(part1)
    cleaned.append([part1, numbers])


# FIRST BOTCHED ATTEMPT - failed for 16931: 568 2 9 16 529 1 8 1 3 8:

def solve(this_target, options, running_total):
    if not options:
        return running_total == this_target
    removed = options[0]
    remainder = options[1:]
    return any([
        solve(this_target, remainder, running_total + removed),
        solve(this_target, remainder, running_total * removed),
    ])


count = 0
for cleaned_item in cleaned:
    target = cleaned_item[0]
    made_from = cleaned_item[1]
    if solve(target, made_from, 0):
        count += target
print(f"BOTCHED FIRST SOLUTION: {count}")

# solution part 1
long_counter = 0
for cleaned_item in cleaned:
    choices = [cleaned_item[1][0]]
    expectation = cleaned_item[0]
    for j in range(len(cleaned_item[1]) - 1):
        next_item = cleaned_item[1][j + 1]
        c0 = [i + next_item for i in choices]
        c1 = [i * next_item for i in choices]
        choices = c0 + c1
    result = [clean for clean in choices if clean == expectation]
    if result:
        long_counter += expectation
print(f"TRUE FIRST SOLUTION: {long_counter}")

# solution part 2
long_counter = 0
for cleaned_item in cleaned:
    choices = [cleaned_item[1][0]]
    expectation = cleaned_item[0]
    for j in range(len(cleaned_item[1]) - 1):
        next_item = cleaned_item[1][j + 1]
        c0 = [i + next_item for i in choices]
        c1 = [i * next_item for i in choices]
        c2 = [int(str(i) + str(next_item)) for i in choices]
        choices = c0 + c1 + c2
    result = [clean for clean in choices if clean == expectation]
    if result:
        long_counter += expectation

# print(count)
print(f"TRUE SECOND SOLUTION: {long_counter}")