import math
import wx
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import networkx as nx
from matplotlib.backend_bases import MouseButton
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class GraphPanel(wx.Panel):
    def __init__(self, panel, menuservice, datastorage):
        wx.Panel.__init__(self, panel, -1)

        self.parent = panel
        self.mservice = menuservice
        self.storage = datastorage

        self.selectednode = None
        self.y_min_node = None
        self.y_max_node = None
        # limits as -x, x, -y, y
        self.borders = (0, 0, 0, 0)
        self.drag_borders = (0, 0, 0, 0)

        plt.rcParams["figure.figsize"] = [1, 3]
        self.figure, self.axes = plt.subplots()
        mplstyle.use('fast')

        self.graph = nx.Graph()
        nx.draw(self.graph)
        self.node_positions = []
        self.color_map = []
        self.labels = []

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        def onclick(event):

            if event.inaxes and event.button == MouseButton.LEFT:
                for n in self.graph.nodes:
                    if euclidiandistance(self.graph.nodes[n]["pos"], (event.xdata, event.ydata)) < 0.1:
                        if "anchor" in n:
                            return
                        self.selectednode = n
                        self.update_borders(n)
                        break
            elif event.button == MouseButton.RIGHT:
                self.mservice.graph_menu()

        def ondrag(event):
            if event.inaxes and self.selectednode is not None:

                x = event.xdata
                y = event.ydata

                node_buffer = 0.2

                if x < self.drag_borders[0]:
                    x = self.drag_borders[0]
                if x > self.drag_borders[1]:
                    x = self.drag_borders[1]
                if y > self.drag_borders[2] - node_buffer:
                    if self.selectednode == self.y_min_node:
                        y = -self.borders[2]
                    else:
                        y = self.drag_borders[2] - node_buffer

                if y < self.drag_borders[3] + node_buffer:
                    if self.selectednode == self.y_max_node:
                        y = -self.borders[3]
                    else:
                        y = self.drag_borders[3] + node_buffer

                self.graph.nodes[self.selectednode]["pos"] = (x, y)
                self.node_positions[self.selectednode] = (x, y)
                plt.clf()
                nx.draw(self.graph, pos=self.node_positions, node_color=self.color_map, with_labels=False, alpha=None)
                nx.draw_networkx_labels(self.graph, pos=self.node_positions, labels=self.labels)
                self.figure.canvas.draw()

        def onrelease(event):
            self.selectednode = None
            self.drag_borders = self.borders

        self.figure.canvas.mpl_connect('button_press_event', onclick)
        self.figure.canvas.mpl_connect('motion_notify_event', ondrag)
        self.figure.canvas.mpl_connect('button_release_event', onrelease)

        def euclidiandistance(a, b):
            return math.sqrt((a[0] -b[0])**2 + (a[1] -b[1])**2)

    def draw_graph(self, graph, borders, y_min_node, y_max_node):

        plt.figure(self.figure.number)

        self.borders = borders
        self.y_min_node = y_min_node
        self.y_max_node = y_max_node

        plt.clf()
        self.graph = graph
        self.node_positions = nx.get_node_attributes(self.graph, 'pos')
        self.labels = nx.get_node_attributes(self.graph, 'label')
        self.color_map.clear()
        for i in range(self.graph.number_of_nodes()):
            if i >= self.graph.number_of_nodes()-4:
                self.color_map.append("None")
            else:
                self.color_map.append("red")
        nx.draw(graph, pos=self.node_positions, node_color=self.color_map,  with_labels=False, alpha=None)
        nx.draw_networkx_labels(graph, pos=self.node_positions, labels=self.labels)
        self.figure.canvas.draw()

    def update_borders(self, node):

        x_min = self.borders[0]
        x_max = self.borders[1]
        y_min = -self.borders[2]
        y_max = -self.borders[3]

        #y_min
        for edge in self.storage.lattice['edges']:
            for start, targets in edge.items():
                if node in targets:
                    if self.node_positions[start][1] < y_min:
                        y_min = self.node_positions[start][1]

        # y_max
        for edge in self.storage.lattice['edges']:
            for start, targets in edge.items():
                if start == node:
                    for target in targets:
                        if self.node_positions[target][1] > y_max:
                            y_max = self.node_positions[target][1]

        self.drag_borders = (x_min, x_max, y_min, y_max)



