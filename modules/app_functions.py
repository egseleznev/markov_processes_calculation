from main import *
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from .db_functions import *
import pickle

class AppFunctions(MainWindow):
    def setThemeHack(self):
        Settings.BTN_LEFT_BOX_COLOR = "background-color:rgb(168, 166, 255)"
        Settings.BTN_RIGHT_BOX_COLOR = "background-color:rgb(168, 166, 255)"
        Settings.MENU_SELECTED_STYLESHEET = MENU_SELECTED_STYLESHEET = """
        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgb(168, 166, 255), stop:0.5 rgb(168, 166, 255));
        background-color: rgb(168, 166, 255);
        """
        
    def serialize(self, path:str ):
        with open(path,'wb') as outfile:
            pickle.dump(DBFunctions.select(self),outfile)

    def deserialize(self, path:str):
        with open(path,'rb') as infile:
            data=pickle.load(infile)
        for i in range(len(data)):
            DBFunctions.insert(self, str(data[i])[0], str(data[i])[2],
                               str(data[i])[4])


    def drawgraph(self):
        vertex_union = []
        from_vertex = list([])
        to_vertex = list([])
        weights_vertex = list([])
        data=DBFunctions.select(self)
        for i in range(len(data)):
            from_vertex.append(str(data[i])[0])
            to_vertex.append(str(data[i])[2])
            weights_vertex.append(str(data[i])[4])
        vertex_union = []
        for i in range(len(from_vertex)):
            vertex_union.append([from_vertex[i], to_vertex[i], weights_vertex[i]])
        Graph = nx.DiGraph()
        Graph.add_weighted_edges_from(vertex_union)
        labels = nx.get_edge_attributes(Graph, 'weight')
        pos = nx.planar_layout(Graph)
        nx.draw_networkx_nodes(Graph, pos, node_size=300)
        nx.draw_networkx_edges(Graph, pos, edgelist=Graph.edges(), edge_color='black')
        nx.draw_networkx_edge_labels(Graph, pos, edge_labels=labels)
        nx.draw_networkx_labels(Graph, pos)
        nx.draw
        plt.savefig("graph.png", dpi=125)
        plt.clf()
        from_vertex.clear()
        to_vertex.clear()
        weights_vertex.clear()

    def calculate(self):
        from_vertex = list([])
        to_vertex = list([])
        weights_vertex = list([])
        data = DBFunctions.select(self)
        for i in range(len(data)):
            from_vertex.append(int(str(data[i])[0]))
            to_vertex.append(int(str(data[i])[2]))
            weights_vertex.append(int(str(data[i])[4]))
        concat = np.hstack((to_vertex, from_vertex))
        unique_numbers = list(set(concat))
        kolmagorov_coefs = np.zeros((len(unique_numbers), len(unique_numbers)))
        for i in range(len(unique_numbers)):
            for j in range(len(from_vertex)):
                if from_vertex[j] == unique_numbers[i]:
                    kolmagorov_coefs[i, from_vertex[j] - 1] = kolmagorov_coefs[i, from_vertex[j] - 1] - weights_vertex[
                        j]
            for k in range(len(to_vertex)):
                if to_vertex[k] == unique_numbers[i]:
                    kolmagorov_coefs[i, from_vertex[k] - 1] = kolmagorov_coefs[i, from_vertex[k] - 1] + weights_vertex[
                        k]
        kolmagorov_coefs[len(kolmagorov_coefs) - 1, :] = 1
        normalization = np.zeros((len(unique_numbers)))
        normalization[len(unique_numbers) - 1] = 1
        result = np.linalg.solve(kolmagorov_coefs, normalization)
        return result
