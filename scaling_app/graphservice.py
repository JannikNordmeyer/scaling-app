import networkx as nx


class GraphService:

    def __init__(self, frame, datastorage):
        self.frame = frame
        self.datastorage = datastorage

    def draw_lattice(self, evt=None):

        if self.datastorage.lattice is None:
            return

        graph = nx.Graph()

        for node in self.datastorage.lattice['positions']:
            for name, coords in node.items():
                graph.add_node(name , pos=(coords[0],coords[1]))

        for edges in self.datastorage.lattice['edges']:
            for origin in edges:
                for target in edges[origin]:
                    graph.add_edge(origin, target)

        self.frame.graph.draw_graph(graph)


    def clear(self, evt=None):

        self.datastorage.lattice = None
        graph = nx.Graph()
        self.frame.graph.draw_graph(graph)


