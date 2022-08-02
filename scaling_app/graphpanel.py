import time

import matplotlib.pyplot as plt
import netgraph
import networkx as nx
import numpy as np
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.figure import Figure
from numpy import arange, sin, pi
from numpy.random import rand
from pyvis.network import Network
import scipy.spatial
import math
import matplotlib.style as mplstyle


class MyNavigationToolbar(NavigationToolbar2WxAgg):

    def __init__(self, canvas, cankill):
        NavigationToolbar2WxAgg.__init__(self, canvas)


class GraphPanel(wx.Panel):
    def __init__(self, panel):
        wx.Panel.__init__(self, panel, -1)

        self.parent = panel

        self.selectednode = None

        plt.rcParams["figure.figsize"] = [1, 3]
        self.figure, self.axes = plt.subplots()
        mplstyle.use('fast')


        self.graph = nx.Graph()
        self.graph.add_node(0, pos=(0, 0))
        self.graph.add_node(1, pos=(0, 1))
        self.graph.add_node(2, pos=(-0.5, 2))
        self.graph.add_node(3, pos=(0.5, 2))
        self.graph.add_node(4, pos=(-0.5, 3))
        self.graph.add_node(5, pos=(0.5, 3))
        self.graph.add_node(6, pos=(0, 4))
        self.graph.add_edge(4, 6)
        self.graph.add_edge(5, 6)
        self.graph.add_edge(2, 5)
        self.graph.add_edge(3, 4)
        self.graph.add_edge(3, 5)
        self.graph.add_edge(0, 3)
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)

        self.pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, self.pos, with_labels=True)

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        def onclick(event):
            if event.inaxes:

                for n in self.graph.nodes:
                    if euclidiandistance(self.graph.nodes[n]["pos"], (event.xdata, event.ydata)) < 0.1:
                        self.selectednode = n
                        break

        def ondrag(event):
            if event.inaxes and self.selectednode is not None:

                self.graph.nodes[self.selectednode]["pos"] = (event.xdata, event.ydata)
                self.pos[self.selectednode] = (event.xdata, event.ydata)
                plt.clf()
                nx.draw(self.graph, self.pos, with_labels=True)
                self.figure.canvas.draw()

        def onrelease(event):
            self.selectednode = None

        self.figure.canvas.mpl_connect('button_press_event', onclick)
        self.figure.canvas.mpl_connect('motion_notify_event', ondrag)
        self.figure.canvas.mpl_connect('button_release_event', onrelease)

        def euclidiandistance(a, b):
            return math.sqrt((a[0] -b[0])**2 + (a[1] -b[1])**2)



        


