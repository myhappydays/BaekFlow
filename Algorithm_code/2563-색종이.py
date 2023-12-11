Paper = [[0 for _ in range(101)] for _ in range(101)]
I = int(input())
Color_Paper = [list(map(int, input().split())) for _ in range(I)]

for i in Color_Paper:
    for a in range(i[0], i[0] + 10):
        for b in range(i[1], i[1] + 10):
            Paper[a][b] = 1

print(sum([Paper[i].count(1) for i in range(101)]))