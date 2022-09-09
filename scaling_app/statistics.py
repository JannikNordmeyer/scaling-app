import wx
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import numpy as np


class StatsPanel(wx.Panel):

    def __init__(self, panel, datastorage):
        wx.Panel.__init__(self, panel, -1)

        self.parent = panel
        self.storage = datastorage

        plt.rcParams["figure.figsize"] = [1, 3]
        self.figure, self.axes = plt.subplots()
        mplstyle.use('fast')

        self.canvas = FigureCanvas(self, -1, self.figure)

        options = ['Histogram', 'Pie Chart']
        cb = wx.ComboBox(self, choices=options, style=wx.CB_READONLY)
        cb.SetSelection(0)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(cb, 1, wx.TOP | wx.LEFT)
        self.sizer.Add(self.canvas, 15, wx.TOP | wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

    def load_histogram(self, values, counts):

        height = list()
        for value in values:
            height.append(counts[value])

        x = np.arange(len(values))
        plt.bar(x, height=height)
        plt.xticks(x, values)
        plt.ylabel('Frequency')
        plt.xlabel('Objects')

    def load_pie(self):
        print("pie")
