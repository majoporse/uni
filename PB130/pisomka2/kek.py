

from math import degrees, atan2


pic = [[4,4,4,4,4,4],
       [4,6,6,6,2,4],
       [4,6,6,6,2,4],
       [4,4,6,2,2,4],
       [4,2,2,2,2,4],
       [4,4,4,4,4,4]]
res = []
for _ in range(len(pic)):
    res.append([None for _ in range(len(pic))])

for y in range(1,len(pic)-1):
    for x in range(1,len(pic[0]) - 1):
        dx = (pic[y][x+1] - pic[y][x-1]) / 2
        dy = (pic[y+1][x] - pic[y-1][x]) / 2
        res[y][x] = degrees(atan2(dy, dx))
print("a")

for y in range(len(pic)):
    str = ""
    for x in range(len(pic)):
        str += " {} ".format(res[y][x])
    print(str)