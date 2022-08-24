import networkx as nx


class GraphService:

    def __init__(self, frame, datastorage):
        self.frame = frame
        self.datastorage = datastorage

    def draw_lattice(self, evt=None):

        if self.datastorage.lattice is None:
            return

        graph = nx.Graph()

        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0

        for node in self.datastorage.lattice['positions']:
            for name, coords in node.items():
                if coords[0] < x_min:
                    x_min = coords[0]
                if coords[0] > x_max:
                    x_max = coords[0]
                if coords[1] < y_min:
                    y_min = coords[1]
                if coords[1] > y_max:
                    y_max = coords[1]

                graph.add_node(name, pos=(coords[0], -coords[1]), color="blue", label=name)

        for edges in self.datastorage.lattice['edges']:
            for origin in edges:
                for target in edges[origin]:
                    graph.add_edge(origin, target)

        graph.add_node("anchor0", pos=(x_min-0.05, -y_min+0.05), color="red", label="")
        graph.add_node("anchor1", pos=(x_max+0.05, -y_min+0.05), color="red", label="")
        graph.add_node("anchor2", pos=(x_min-0.05, -y_max-0.05), color="red", label="")
        graph.add_node("anchor3", pos=(x_max+0.05, -y_max-0.05), color="red", label="")

        self.frame.graph.draw_graph(graph, (x_min, x_max, y_min, y_max))

    def clear(self, evt=None):

        self.datastorage.lattice = None
        graph = nx.Graph()
        self.frame.graph.draw_graph(graph, (0, 0, 0, 0))


