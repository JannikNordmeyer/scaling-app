import math
import time
import wx
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import networkx as nx
from matplotlib.backend_bases import MouseButton
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure


class GraphPanel(wx.Panel):
    def __init__(self, panel, menuservice, datastorage):
        wx.Panel.__init__(self, panel, -1)

        self.parent = panel
        self.mservice = menuservice
        self.storage = datastorage

        self.selectednode = None
        # limits as -x, x, -y, y
        self.borders = (0, 0, 0, 0)

        plt.rcParams["figure.figsize"] = [1, 3]
        self.figure, self.axes = plt.subplots()
        mplstyle.use('fast')
        print(self.axes.get_xlim())
        print(self.axes.get_xbound())
        self.axes.set_autoscale_on(False)
        print(self.axes.get_autoscale_on())

        self.graph = nx.Graph()
        nx.draw(self.graph)
        self.node_positions = []

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        def onclick(event):

            print(event.ydata)
            if event.inaxes and event.button == MouseButton.LEFT:

                for n in self.graph.nodes:
                    if euclidiandistance(self.graph.nodes[n]["pos"], (event.xdata, event.ydata)) < 0.1:
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

                if x < self.borders[0]:
                    x = self.borders[0]
                if x > self.borders[1]:
                    x = self.borders[1]
                if y > self.borders[2] - node_buffer:
                    y = self.borders[2] - node_buffer
                if y < self.borders[3] + node_buffer:
                    y = self.borders[3] + node_buffer

                self.graph.nodes[self.selectednode]["pos"] = (x, y)
                self.node_positions[self.selectednode] = (x, y)
                plt.clf()
                nx.draw(self.graph, self.node_positions, with_labels=True)
                self.figure.canvas.draw()

        def onrelease(event):
            self.selectednode = None

        self.figure.canvas.mpl_connect('button_press_event', onclick)
        self.figure.canvas.mpl_connect('motion_notify_event', ondrag)
        self.figure.canvas.mpl_connect('button_release_event', onrelease)

        def euclidiandistance(a, b):
            return math.sqrt((a[0] -b[0])**2 + (a[1] -b[1])**2)

    def draw_graph(self, graph, borders):

        self.borders = borders

        plt.clf()
        self.graph = graph
        self.node_positions = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(graph, self.node_positions, with_labels=True)
        self.figure.canvas.draw()

    def update_borders(self, node):

        x_min = self.borders[0]
        x_max = self.borders[1]
        y_min = self.borders[2]
        y_max = self.borders[3]

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
                        if self.node_positions[target][1] < y_max:
                            y_max = self.node_positions[target][1]

        self.borders = (x_min, x_max, y_min, y_max)



