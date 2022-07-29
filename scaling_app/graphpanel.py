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
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from numpy import arange, sin, pi
from matplotlib.backends.backend_wx import _load_bitmap


class MyNavigationToolbar(NavigationToolbar2WxAgg):
    """
    Extend the default wx toolbar with your own event handlers
    """
    ON_CUSTOM = wx.NewId()

    def __init__(self, canvas, cankill):
        NavigationToolbar2WxAgg.__init__(self, canvas)

        # for simplicity I'm going to reuse a bitmap from wx, you'll
        # probably want to add your own.
        if 'phoenix' in wx.PlatformInfo:
            self.AddTool(self.ON_CUSTOM, 'Click me',
                         _load_bitmap('back.png'),
                         'Activate custom contol')
            self.Bind(wx.EVT_TOOL, self._on_custom, id=self.ON_CUSTOM)
        else:
            self.AddSimpleTool(self.ON_CUSTOM, _load_bitmap('back.png'),
                               'Click me', 'Activate custom contol')
            self.Bind(wx.EVT_TOOL, self._on_custom, id=self.ON_CUSTOM)

    def _on_custom(self, evt):
        # add some text to the axes in a random location in axes (0,1)
        # coords) with a random color

        # get the axes
        ax = self.canvas.figure.axes[0]

        # generate a random location can color
        x, y = tuple(rand(2))
        rgb = tuple(rand(3))

        # add the text and draw
        ax.text(x, y, 'You clicked me',
                transform=ax.transAxes,
                color=rgb)
        self.canvas.draw()
        evt.Skip()


class GraphPanel(wx.Panel):
    def __init__(self, panel):
        wx.Panel.__init__(self, panel, -1)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.axes = self.figure.add_subplot(111)
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)

        self.axes.plot(t, s)

        self.canvas = FigureCanvas(self, -1, self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)
        # Capture the paint message
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.toolbar = MyNavigationToolbar(self.canvas, True)
        self.toolbar.Realize()
        # By adding toolbar in sizer, we are able to put it at the bottom
        # of the frame - so appearance is closer to GTK version.
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)

        # update the axes menu on the toolbar
        self.toolbar.update()
        self.SetSizer(self.sizer)
        self.Fit()

    def OnPaint(self, event):
        self.canvas.draw()
        event.Skip()


        


