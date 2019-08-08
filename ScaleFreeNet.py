import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random


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

    def generate_exponential_network(self, p=0.7, m=1, n=10, save=False, filename='', show=True):

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
