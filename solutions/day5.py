with open("../inputs/day5.txt") as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]


def get_middle_value(list_in):
    position = (len(list_in) - 1) // 2
    return list_in[position]


def check_rule_broken(list_in, rule):
    if (rule[0] not in list_in) or (rule[1] not in list_in):
        return False
    for value in list_in:
        if value == rule[1]:
            return True
        elif value == rule[0]:
            return False


rules = []
updates = []
for line in lines:
    if "|" in line:
        rules.append(line)
    elif line != "":
        updates.append(line)

rules = [rule.split("|") for rule in rules]
for rule in rules:
    rule[0] = int(rule[0])
    rule[1] = int(rule[1])

updates = [update.split(",") for update in updates]
for i in range(len(updates)):
    updates[i] = [int(update) for update in updates[i]]

good_list = list()
for value in updates:
    rules_broken = False
    for rule in rules:
        if check_rule_broken(value, rule):
            rules_broken = True
    if not rules_broken:
        good_list.append(value)

count = 0
for value in good_list:
    count += get_middle_value(value)

print(count)