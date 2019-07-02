from RandomNet import RandomNetwork
import numpy as np
import re


def f(A, i):
    temp = []
    if i == A.shape[1]:
        temp.append('0')
    else:
        temp.append('1')
        i -= 1
        for j in range(A.shape[1]):
            if A[i][j] != 0:
                temp.append('C{}'.format(j + 1))
    return temp


def cascade(A, i):

    status = False
    node = []
    total = 0
    a = []

    while not status:

        a += f(A, i)
        a = list(set(a))
        a = sorted(a)
        j = 0
        while j < len(a) and 'C' not in a[j]:
            j += 1

        if j >= len(a):
            status = True
        else:
            i = int(re.sub(r'[^0-9]', '', a[j]))
            temp = a[:j]
            total += sum(list(map(int, temp)))
            a = a[j:]
            while len(a) > 0 and i in node:
                a.pop(0)
                if len(a) > 0:
                    i = int(re.sub(r'[^0-9]', '', a[0]))
                else:
                    status = True
            node.append(i)

    return total, sorted(list(set(node)))


if __name__ == '__main__':

    # A = np.array([[0, 1, 0, 0, 1], [0, 0, 1, 1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]])
    rn = RandomNetwork()
    # A = rn.generate_random_network(p=0.6, n=10, save=True)
    A = rn.loadcsv('Saved matrix/Graph_p=0.6_N=10.csv')
    rn.show_graph()
    print(cascade(A, 1))
