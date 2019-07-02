# import the relevant libraries
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np


def rand():
    """
    produces a random value between 0.0 and 1.0

    :return:
    """
    random_number = random.randint(0, 10)
    f_rand = float(random_number)
    d_rand = f_rand * 0.1
    return d_rand


def predicted_number_of_edges(p, N):
    """
    the predicted number of edges: p x N x (N - 1) / 2

    :param p:
    :param N:
    :return:
    """
    return (p * N * (N - 1)) / 2


def generate_random_network(p=0.4, n=10, save=False, filename=''):
    """

    :param p: probability p
    :param n: number of nodes
    :return:
    """

    # lets predict the number of edges
    print("Predicted number of edges: " + str(predicted_number_of_edges(p, n)))

    # our graph
    g = nx.Graph()

    # start with n isolated nodes
    for x in range(0, n):
        g.add_node(x)

    # consider every possible link between each node
    for x in range(0, n):
        # we disregard the last node, because this link has already been considered (#1)
        for y in range(x, n):
            # add it with probability p, unless p=1, in which case add it anyway
            # ensuring the edge is not being added to itself
            if (rand() < p or p == 1.0) & (x != y):
                # we do not need to check to see if the edge already exists, because of #1
                g.add_edge(x, y)

    print("Actual number of edges: " + str(g.number_of_edges()))
    g = g.to_directed()
    A = nx.to_numpy_matrix(g)
    A = np.array(A)
    for i in range(len(A)):
        for j in range(i+1):
            A[i][j] = 0

    D = nx.DiGraph(A)
    D = nx.convert_node_labels_to_integers(D, first_label=1)

    # lets draw this lovely thing!
    nx.draw(D, pos=nx.spring_layout(D), with_labels=True, nodelist=D.node)
    plt.show()

    return A