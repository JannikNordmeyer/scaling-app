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

        self.values = None
        self.counts = None

        self.figure, self.axes = plt.subplots()
        mplstyle.use('fast')

        self.canvas = FigureCanvas(self, -1, self.figure)

        options = ['Histogram', 'Pie Chart']
        self.combobox = wx.ComboBox(self, choices=options, style=wx.CB_READONLY)
        self.combobox.SetSelection(0)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.combobox, 1, wx.TOP | wx.LEFT)
        self.sizer.Add(self.canvas, 15, wx.TOP | wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        self.combobox.Bind(wx.EVT_COMBOBOX, self.select)

    def select(self, evt):

        plt.clf()

        if evt.GetSelection() == 0:
            self.load_histogram(self.values, self.counts)
        if evt.GetSelection() == 1:
            self.load_pie(self.values, self.counts)

    def load_histogram(self, values, counts):

        height = list()
        for value in values:
            height.append(counts[value])
        self.values = values
        self.counts = counts

        x = np.arange(len(values))
        plt.bar(x, height=height)
        plt.xticks(x, values)
        plt.ylabel('Frequency')
        plt.xlabel('Objects')

        self.figure.canvas.draw()

    def load_pie(self, values, counts):

        height = list()
        for value in values:
            height.append(counts[value])
        self.values = values
        self.counts = counts

        plt.pie(height, labels=values, autopct='%1.1f%%',
                shadow=True, startangle=90)

        self.figure.canvas.draw()

