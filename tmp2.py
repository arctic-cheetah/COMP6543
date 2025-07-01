def rotate(l, n):
    return l[n:] + l[:n]


print(rotate([1, 2, 3, 4, 5], 1))
