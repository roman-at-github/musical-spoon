'''
Uses a graph-file as input and creates a Graph-Object out of Vertex and Edge Objects
'''
from Vertex import Vertex
from Edge import Edge
from Graph import Graph


def parse(filename):

    # Properties of the graph. Characterized in the first block of a graph-file
    n_of_nodes = 0
    n_of_edges = 0
    nodes_label = False
    edges_label = False
    directed_graph = False

    # Vertex list is characterized in the 2nd block of a graph-file
    vertex_list = []

    # Edge list is characterized in the 3rd block of a graph-file
    edge_list = []

    # c is a counter to know in which block of the graph-file we are
    c = 0

    with open(filename, 'r') as file:
        file_content = file.readlines()
        for i in range(0, len(file_content)):
            temp = file_content[i].replace('\n', '').split(';')
            if temp == ['']:
                c += 1
            elif temp is not '' and c == 0:
                if temp[0] == '#nodes':
                    n_of_nodes = temp[1]
                elif temp[0] == '#edges':
                    n_of_edges = temp[1]
                elif temp[0] == 'Nodes labelled':
                    if temp[1] == 'True':
                        nodes_label = True
                    else:
                        nodes_label = False
                elif temp[0] == 'Edges labelled':
                    if temp[1] == 'True':
                        edges_label = True
                    else:
                        edges_label = False
                elif temp[0] == 'Directed graph':
                    if temp[1] == 'True':
                        directed_graph = True
                    else:
                        directed_graph = False
            elif c == 1:
                v = Vertex(temp[0])
                if nodes_label:
                     v.set_node_label(temp[1])
                vertex_list.append(Vertex(temp[0]))
            elif c == 2:
                e = Edge(temp[0], temp[1])  # unnoetig, weil Edge-Objekt 3 Zeilen weiter unten erstellt wird
                if edges_label:             # funktioniert so auch noch nicht
                    e.set_label(temp[2])
                edge_list.append(Edge(vertex_list[(int(temp[0])-1)], vertex_list[(int(temp[1])-1)]))    # so funktioniert das nur solange die reihenfolge zufällig stimmt und solange die kanten Nummern als Namen haben

    graph = Graph(vertex_list, edge_list)
    return graph




