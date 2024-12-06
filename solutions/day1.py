import re

with open("advent_of_code.txt") as f:
    lines = f.readlines()

l1 = []
l2 = []
for line in lines:
    search = re.search("^(\d+)\s+(\d+)$", line)
    l1.append(int(search.group(1)))
    l2.append(int(search.group(2)))

l1 = sorted(l1)
l2 = sorted(l2)

res = 0
for i in range(len(l1)):
    res += l1[i] * l2.count(l1[i])
print(res)
