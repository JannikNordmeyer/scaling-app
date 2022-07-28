from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas, NavigationToolbar2WxAgg as NavigationToolbar
import matplotlib.pyplot as plt
import wx
import networkx as nx


class GraphPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.fig = plt.figure()
        self.canvas = FigureCanvas(parent, -1, self.fig)
        G=nx.house_graph()
        pos={0:(0,0),
            1:(1,0),
            2:(0,1),
            3:(1,1),
            4:(0.5,2.0)}

        nx.draw_networkx_nodes(G,pos,node_size=2000,nodelist=[4])
        nx.draw_networkx_nodes(G,pos,node_size=3000,nodelist=[0,1,2,3],node_color='r')
        nx.draw_networkx_edges(G,pos,alpha=0.5,width=6)
        plt.axis('off')
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.toolbar = NavigationToolbar(self.canvas)
        self.vbox.Add(self.toolbar, 0, wx.EXPAND)
        parent.SetSizer(self.vbox)
        self.vbox.Fit(self)
