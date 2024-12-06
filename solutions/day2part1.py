with open("../inputs/day2part1.txt") as f:
    text = f.readlines()


def is_safe_sequence(sequence):
    if len(sequence) <= 1:
        return True
    direction = sequence[1] - sequence[0]
    if direction > 0:
        increasing = True
    elif direction < 0:
        increasing = False
    else:
        return False
    is_safe = True
    for j in range(len(sequence) - 1):
        if not all([
            abs(sequence[j + 1] - sequence[j]) in [1, 2, 3],
            sequence[j + 1] > sequence[j] if increasing else sequence[j + 1] < sequence[j],
        ]):
            is_safe = False
    return is_safe


safe = 0
for line in text:
    values = [int(i) for i in line.split()]
    permutations = [values[: i] + values[i + 1:] for i in range(len(values))]
    print(permutations)
    good_count = 0
    for permutation in permutations:
        good_count += is_safe_sequence(permutation)
    if good_count >= 1:
        safe += 1
    print(good_count >= 1)
print(safe)