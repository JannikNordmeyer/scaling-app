import wx
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import numpy as np


class StatsPanel(wx.Panel):

    def __init__(self, panel, datastorage, attribute):
        wx.Panel.__init__(self, panel, -1)

        self.parent = panel
        self.storage = datastorage

        self.attribute = attribute

        self.values = None
        self.counts = None
        self.selection = 0

        self.figure, self.axes = plt.subplots()
        mplstyle.use('fast')

        self.canvas = FigureCanvas(self, -1, self.figure)

        options = ['Histogram', 'Pie Chart']
        self.combobox = wx.ComboBox(self, choices=options, style=wx.CB_READONLY)
        self.combobox.SetSelection(0)

        self.infotext = wx.StaticText(self)
        font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.infotext.SetFont(font)
        self.infotext.SetLabel("")


        self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer.Add(self.combobox, 1, wx.TOP | wx.LEFT)
        self.hsizer.Add(self.infotext, 1, wx.TOP | wx.LEFT)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.hsizer, 1, wx.TOP | wx.LEFT)
        self.sizer.Add(self.canvas, 15, wx.TOP | wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        self.combobox.Bind(wx.EVT_COMBOBOX, self.select)

    def select(self, evt):

        self.selection = evt.GetSelection()

        self.load_stats(evt.GetSelection())

    def load_stats(self, selection):

        plt.clf()
        if selection == 0:
            self.load_histogram(self.values, self.counts)
        if selection == 1:
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


