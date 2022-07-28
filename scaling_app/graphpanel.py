from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import matplotlib.pyplot as plt
import wx
import networkx as nx
import netgraph
import numpy as np
from netgraph import InteractiveGraph
import networkx as nx


class GraphPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure(figsize=(4, 7), dpi=100)
        self.axes = self.figure.add_subplot(111)

        G = nx.path_graph(10)
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, ax=self.axes)
        I = netgraph.InteractiveGraph(G)

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)

        


