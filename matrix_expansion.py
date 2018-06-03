"""
Module that expands a bidimensional matrix and finds the surroundings
of any position in this matrix.
"""

def expandMatrix(mat, times=1, e=None):
    """
    Expands the matrix from the outside, as many times as necessary.
    The elements added due to the expansion are None by default.
    """
    mat2 = [row[:] for row in mat]

    line = [e for i in range(len(mat2[0]) + (times*2))]
    for v in range(times):
        mat2.insert(0, line)
        mat2.append(line)

    for i in range(times, len(mat2)-times):
        for v in range(times):
            mat2[i].insert(0, e)
            mat2[i].append(e)

    return mat2

def findSurroundings(mat, p, order=1):
    """
    Find the surrounding positions of a certain position in the matrix.
    The surroundings have order 1 by default.
    In order to do this, expands the matrix as many times as the surroundings
    order, to avoid problems with positions in the corner of the matrix.
    """
    mat2 = [row[:] for row in mat]

    if order <= 0: return [p]

    mat2 = expandMatrix(mat2, order)

    #goes through the matrix and find the surroundings
    surr = []

    start1 = (p[0], p[1])
    start2 = (start1[0], start1[1] + order*2)
    start3 = (start2[0] + order*2, start2[1])
    start4 = (start3[0], start3[1] - order*2)

    for j in range(start1[1], start2[1]):
        if mat2[start1[0]][j] is not None:
            surr.append([start1[0], j])

    for i in range(start2[0], start3[0]):
        if mat2[i][start2[1]] is not None:
            surr.append([i, start2[1]])

    for j in range(start3[1], start4[1], -1):
        if mat2[start3[0]][j] is not None:
            surr.append([start3[0], j])

    for i in range(start4[0], start1[0], -1):
        if mat2[i][start4[1]] is not None:
            surr.append([i, start4[1]])

    #convert positions so that they are
    #compatible with the original matrix
    for pos in surr:
        pos[0] -= order
        pos[1] -= order

    return surr
