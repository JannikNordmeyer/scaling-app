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
    def __init__(self, panel, menuservice):
        wx.Panel.__init__(self, panel, -1)

        self.parent = panel
        self.mservice = menuservice

        self.selectednode = None

        plt.rcParams["figure.figsize"] = [1, 3]
        self.figure, self.axes = plt.subplots()
        mplstyle.use('fast')

        self.graph = nx.Graph()
        nx.draw(self.graph)
        self.node_positions = []

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        def onclick(event):

            if event.inaxes and event.button == MouseButton.LEFT:

                for n in self.graph.nodes:
                    if euclidiandistance(self.graph.nodes[n]["pos"], (event.xdata, event.ydata)) < 0.1:
                        self.selectednode = n
                        break
            elif event.button == MouseButton.RIGHT:
                self.mservice.graph_menu()

        def ondrag(event):
            if event.inaxes and self.selectednode is not None:

                self.graph.nodes[self.selectednode]["pos"] = (event.xdata, event.ydata)
                self.node_positions[self.selectednode] = (event.xdata, event.ydata)
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

    def draw_graph(self, graph):

        plt.clf()
        self.graph = graph
        self.node_positions = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(graph, self.node_positions, with_labels=True)
        self.figure.canvas.draw()
