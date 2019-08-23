import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random


class RandomNetwork(object):

    def __init__(self):
        self.g = None
        self.A = None
        self.D = None

    def rand(self):
        """
        produces a random value between 0.0 and 1.0

        :return:
        """
        random_number = random.randint(0, 10)
        f_rand = float(random_number)
        d_rand = f_rand * 0.1
        return d_rand

    def predicted_number_of_edges(self, p, N):
        """
        the predicted number of edges: p x N x (N - 1) / 2

        :param p:
        :param N:
        :return:
        """
        return (p * N * (N - 1)) / 2

    def loadcsv(self, filename):
        self.A = np.loadtxt(open(filename, 'rb'), delimiter=',')
        return self.A

    def show_graph(self):
        self.D = nx.DiGraph(self.A)
        self.D = nx.convert_node_labels_to_integers(self.D, first_label=1)
        nx.draw(self.D, pos=nx.spring_layout(self.D), with_labels=True, nodelist=self.D.node)
        plt.show()

    def generate_random_network(self, p=0.4, n=10, save=False, filename='', show=True):
        """

        :param p: probability p
        :param n: number of nodes
        :param save:
        :param filename:
        :param show:
        :return:
        """

        # initialize graph
        self.g = nx.Graph()

        # Initialize nodes
        for x in range(0, n):
            self.g.add_node(x)

        # Generate random network
        # consider every possible link between each node
        for x in range(0, n):
            # we disregard the last node, because this link has already been considered (#1)
            for y in range(x, n):
                # add it with probability p, unless p=1, in which case add it anyway
                # ensuring the edge is not being added to itself
                if (self.rand() < p or p == 1.0) & (x != y):
                    # we do not need to check to see if the edge already exists, because of #1
                    self.g.add_edge(x, y)

        # Transform into directed network
        self.g = self.g.to_directed()
        self.A = nx.to_numpy_matrix(self.g)
        self.A = np.array(self.A)
        for i in range(len(self.A)):
            for j in range(i+1):
                self.A[i][j] = 0

        # Show the network
        print("Predicted number of edges: " + str(self.predicted_number_of_edges(p, n)))
        print("Actual number of edges: " + str(self.g.number_of_edges()))

        if show:
            self.show_graph()

        # Save the network, if save parameter is set True
        if save:
            if filename == '':
                np.savetxt("Saved matrix/Graph_p={}_N={}.csv".format(p, n), self.A, delimiter=",")
            else:
                np.savetxt("Saved matrix/{}".format(filename), self.A, delimiter=",")

        return self.A


class ScaleFreeNetwork(object):

    def __init__(self):
        self.G = None
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

    def generate_scale_free_network(self, p=0.7, m=1, n=10, save=False, filename='', show=True):

        self.G = nx.powerlaw_cluster_graph(n, m, p)
        self.A = nx.to_numpy_matrix(self.G)
        self.A = np.array(self.A)
        for i in range(len(self.A)):
            for j in range(i + 1):
                self.A[i][j] = 0

        if show:
            self.show_graph()

        # Save the network, if save parameter is set True
        if save:
            if filename == '':
                np.savetxt("Saved matrix/Graph_p={}_N={}.csv".format(p, n), self.A, delimiter=",")
            else:
                np.savetxt("Saved matrix/{}".format(filename), self.A, delimiter=",")

        return self.A


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

    def generate_exponential_network(self, p=1, d=2, m=5, n=10, save=False, filename='', show=True):
        """

        :param p: probability p, default 1
        :param m: number of nodes
        :param d:
        :param n:
        :param save:
        :param filename:
        :param show:
        :return:
        """

        # initialize graph
        self.g = nx.DiGraph()

        # Initialize nodes
        for x in range(0, m):
            self.g.add_node(x)

        while m < n:

            for i in range(d):
                temp_node = random.randint(0, m)
                if temp_node != m and not self.g.has_edge(temp_node, m):
                    self.g.add_edge(temp_node, m)

            m += 1

        self.A = nx.to_numpy_matrix(self.g)
        self.A = np.array(self.A)

        if show:
            self.show_graph()

        # Save the network, if save parameter is set True
        if save:
            if filename == '':
                np.savetxt("Saved matrix/Graph_p={}_N={}.csv".format(p, m), self.A, delimiter=",")
            else:
                np.savetxt("Saved matrix/{}".format(filename), self.A, delimiter=",")

        return self.A
