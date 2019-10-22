from Network import ScaleFreeNetwork, RandomNetwork, ExponentialNetwork
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import json
import sys
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


def multi_cascade(A, n_fail, failure_node=1):

    res = []
    c_list = []
    temp_node = list(range(1, len(A[0]) + 1))
    for ii in range(n_fail):
        # failure_node = temp_node[np.random.randint(1, len(temp_node))]
        n, list_node = cascade(A, failure_node)
        A[failure_node - 1] = 0
        temp_node.remove(failure_node)
        for jj in range(len(list_node)):
            A[:, list_node[jj] - 1] = 0
            A[failure_node - 1, :] = 0
            if list_node[jj] in temp_node:
                temp_node.remove(list_node[jj])
        c_list.append(failure_node)
        c_list += list_node
        c_list = list(set(c_list))
        res.append([failure_node, list_node])
    return A, c_list, res


if __name__ == '__main__':

    p = 1
    d = 2
    m = 5
    c = 2
    n = 1000
    save = False
    filename = ''
    show = False
    n_failure = 1

    for text in sys.argv:
        if '-p=' in text:
            p = float(text[text.index('=') + 1:])

    for text in sys.argv:
        if '-d=' in text:
            d = int(text[text.index('=') + 1:])

    for text in sys.argv:
        if '-m=' in text:
            m = int(text[text.index('=') + 1:])

    for text in sys.argv:
        if '-n=' in text:
            n = int(text[text.index('=') + 1:])

    for text in sys.argv:
        if '-c=' in text:
            c = int(text[text.index('=') + 1:])

    for text in sys.argv:
        if '-f=' in text:
            n_failure = int(text[text.index('=') + 1:])

    for text in sys.argv:
        if '-filename=' in text:
            filename = text[text.index('=') + 1:]

    # for text in sys.argv:
    #     if '-save=' in text:
    #         save = text[text.index('=') + 1:]

    # for text in sys.argv:
    #     if '-show=' in text:
    #         show = text[text.index('=') + 1:]

    # A = np.array([[0, 1, 0, 0, 1], [0, 0, 1, 1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]])

    # Generate Random Network
    # rn = RandomNetwork()
    # A = rn.generate_random_network()

    for ii in range(10):

        # Generate Exponential Network
        # en = ExponentialNetwork()
        # A = en.generate_exponential_network(p=p, d=d, m=m, n=n, save=save, filename=filename, show=show)

        # Generate Scale Free Network
        sf = ScaleFreeNetwork()
        A = sf.generate_scale_free_network(p=p, m=m, n=n)

        A, cascade_list, result = multi_cascade(A, n_failure)
        temp1 = {}
        temp2 = {}
        temp3 = len(cascade_list) - n_failure

        for i in range(len(result)):
            temp1[result[i][0]] = result[i][1]

        for i in range(len(result)):
            temp2[result[i][0]] = len(result[i][1])

        result = {'List node failure': temp1,
                  'Number of node failure': temp2,
                  'Cascade failure': temp3,
                  'Total node failure': len(cascade_list),
                  'p': p,
                  'd': d,
                  'm': m,
                  'n': n,
                  'failure': n_failure
                  }
        print(result['Cascade failure'])

        if filename == '':
            filename = 'network_p={}_d={}_m={}_n={}_f={}_c={}'.format(p, d, m, n, n_failure, c)
        filename = 'C1_D2_{}'.format(ii + 1)
        with open('Saved/{}.json'.format(filename), 'w') as outfile:
            json.dump(result, outfile)

        if show:
            G = nx.DiGraph(A)
            D = nx.convert_node_labels_to_integers(G, first_label=1)
            for i in range(len(cascade_list)):
                D.remove_node(cascade_list[i])
            nx.draw(D, pos=nx.spring_layout(D), with_labels=True, nodelist=D.node)
            plt.show()
