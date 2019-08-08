import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random


class ExponentialNetwork(object):

    def __init__(self):
        self.g = None
        self.A = None
        self.D = None

    def loadcsv(self, filename):
        self.A = np.loadtxt(open(filename, 'rb'), delimiter=',')
        return self.A

    def show_graph(self):
        self.D = nx.DiGraph(self.A)
        self.D = nx.convert_node_labels_to_integers(self.D, first_label=1)
        nx.draw(self.D, pos=nx.spring_layout(self.D), with_labels=True, nodelist=self.D.node)
        plt.show()

    def generate_exponential_network(self, p=1, n=5, d=2, m=10, save=False, filename='', show=True):
        """

        :param p: probability p
        :param n: number of nodes
        :param d:
        :param m:
        :param save:
        :param filename:
        :param show:
        :return:
        """

        # initialize graph
        self.g = nx.DiGraph()

        # Initialize nodes
        for x in range(0, n):
            self.g.add_node(x)

        while n <= m:

            for i in range(d):
                temp_node1 = random.randint(0, n)
                temp_node2 = random.randint(0, n)
                if temp_node1 > temp_node2:
                    temp_node1, temp_node2 = temp_node2, temp_node1
                if temp_node1 != temp_node2 and self.g.has_edge(temp_node1, temp_node2) == False:
                    self.g.add_edge(temp_node1, temp_node2)
            n += 1

        self.A = nx.to_numpy_matrix(self.g)
        self.A = np.array(self.A)

        if show:
            self.show_graph()

        # Save the network, if save parameter is set True
        if save:
            if filename == '':
                np.savetxt("Saved matrix/Graph_p={}_N={}.csv".format(p, n), self.A, delimiter=",")
            else:
                np.savetxt("Saved matrix/{}".format(filename), self.A, delimiter=",")

        return self.A
