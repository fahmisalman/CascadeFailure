from Network import ScaleFreeNetwork, RandomNetwork, ExponentialNetwork
import matplotlib.pyplot as plt
import networkx as nx
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

    list_node = sorted(list(set(node)))

    return len(list_node), list_node


def multi_cascade(A, n_failure):

    result = []
    cascade_list = []
    for i in range(n_failure):
        failure_node = np.random.randint(1, len(A))
        n, list_node = cascade(A, failure_node)
        A[failure_node - 1] = 0
        for j in range(len(list_node)):
            A[failure_node - 1, list_node[j] - 1] = 0
        cascade_list.append(failure_node)
        cascade_list += list_node
        cascade_list = list(set(cascade_list))
        result.append([failure_node, list_node])
    return A, cascade_list, result


if __name__ == '__main__':

    # A = np.array([[0, 1, 0, 0, 1], [0, 0, 1, 1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]])

    # Generate Scale Free Network
    # rn = RandomNetwork()
    # A = rn.generate_random_network()

    # Generate Scale Free Network
    en = ExponentialNetwork()
    A = en.generate_exponential_network()

    # Generate Scale Free Network
    # sf = ScaleFreeNetwork()
    # A = sf.generate_scale_free_network()

    A, cascade_list, result = multi_cascade(A, 2)
    temp = {}

    for i in range(len(result)):
        temp['Node ' + str(result[i][0])] = result[i][1]

    result = {'Result': temp,
              'Total node failure': len(cascade_list),
              'List node failure': cascade_list}
    print(result)

    G = nx.DiGraph(A)
    D = nx.convert_node_labels_to_integers(G, first_label=1)
    nx.draw(D, pos=nx.spring_layout(D), with_labels=True, nodelist=D.node)
    plt.show()
