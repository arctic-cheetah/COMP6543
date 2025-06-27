import copy

arr = [1, 0, 0, 1]
ans1 = copy.deepcopy([1, 0, 0, 0])
ans2 = copy.deepcopy([1, 0, 0, 0])


for x in range(0, 16):
    ans1.insert(x + 4, (ans1[x] + ans1[x + 1]) % 2)
print(ans1)

for x in range(0, 16):
    ans2.insert(x + 4, (ans2[x] + ans2[x + 1] + ans2[x + 3]) % 2)
print(ans2)
