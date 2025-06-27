arr = [1, 0, 0, 1]


for x in range(0, 16):
    arr.insert(x + 4, (arr[x] + arr[x + 1]) % (2))
print(arr)
