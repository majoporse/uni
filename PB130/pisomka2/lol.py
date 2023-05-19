

matrix = [[1, 1, 1, 3, 0, 5, 5, 5],
          [1, 1, 1, 3, 0, 5, 5, 5],
          [1, 1, 1, 3, 0, 5, 5, 5],
          [3, 3, 3, 4, 7, 3, 3, 3],
          [2, 2, 2, 1, 1, 2, 2, 2],
          [2, 2, 2, 1, 1, 2, 2, 2],
          [2, 2, 2, 1, 1, 2, 2, 2]]

kernel1 = [[-2, -1, 2],
          [0, 1, 1],
          [1, -2, 3]]

kernel = [[3, -2, 1],
          [1, 1, 0], 
          [2, -1, -2]]

kerW = len(kernel[0])
kerH = len(kernel)

matW = len(matrix[0])
matH = len(matrix)


result = []

for my in range(0, matH - kerH + 1):
    buff = []
    for  mx in range(0, matW - kerH + 1):
        
        sum = 0
        for ky in range(0, kerH):
            for kx in range(0, kerW):

                ker = kernel[ky][kx]

                mat = matrix[my + ky][mx + kx]
                sum += mat * ker

        buff.append(sum)

    result.append(buff)

for y in range(matH - kerH + 1):
    string = ""
    for x in range(matW - kerW + 1):
        string += "  {}  ".format(result[y][x])
    print(string)

    
			
		