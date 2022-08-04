import wx
import networkx as nx

class GraphService:

    def __init__(self, frame, datastorage):
        self.frame = frame
        self.datastorage = datastorage

    def draw_lattice(self):

        if self.datastorage.context is None:
            return

        graph = nx.Graph()

        for node in self.datastorage.context['positions']:
            for name, coords in node.items():
                graph.add_node(name , pos=(coords[0],coords[1]))

        for edges in self.datastorage.context['edges']:
            for origin in edges:
                for target in edges[origin]:
                    graph.add_edge(origin, target)

        self.frame.graph.draw_graph(graph)



    def redraw_lattice(self, evt=None):
        dc = wx.ClientDC(self.frame.panelLeft)
        dc.Clear()
        self.draw_lattice()

    def clear(self, evt=None):
        dc = wx.ClientDC(self.frame.panelLeft)
        dc.Clear()
        self.datastorage.context = None

