import collections

from matplotlib import pylab

import statistics

import wx
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backend_bases import MouseButton
import numpy as np
from scaling_app import constants


class StatsPanel(wx.Panel):

    def __init__(self, panel, datastorage, menuservice, attribute):
        wx.Panel.__init__(self, panel, -1)

        self.parent = panel
        self.storage = datastorage
        self.mservice = menuservice

        self.attribute = attribute

        self.values = None
        self.counts = None
        self.selection = 0

        self.figure = plt.figure()

        self.canvas = FigureCanvas(self, -1, self.figure)

        options = ['Histogram', 'Pie Chart']
        self.combobox = wx.ComboBox(self, choices=options, style=wx.CB_READONLY)
        self.combobox.SetSelection(0)

        # Text for Central Tendencies
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
        self.figure.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        if event.button == MouseButton.RIGHT:
            self.mservice.stats_menu()

    def select(self, evt):

        # Handle Selection via Combobox
        self.selection = evt.GetSelection()
        self.load_stats(evt.GetSelection())

    def load_stats(self, selection):

        if selection == 0:
            self.load_histogram(self.values, self.counts)
        if selection == 1:
            self.load_pie(self.values, self.counts)

    def load_histogram(self, values, counts):

        plt.figure(self.figure.number)
        plt.clf()

        height = list()
        for value in values:
            height.append(counts[value])
        self.values = values
        self.counts = counts

        sns.set(style="darkgrid")
        sns.barplot(x=values, y=height)

        self.set_tendencies()
        self.figure.canvas.draw()

    def load_pie(self, values, counts):

        plt.figure(self.figure.number)
        plt.clf()

        height = list()
        for value in values:
            height.append(counts[value])
        self.values = values
        self.counts = counts

        plt.pie(height, labels=values, autopct='%1.1f%%',
                shadow=True, startangle=90)

        self.set_tendencies()
        self.figure.canvas.draw()

    def load_histplot(self):
        print("Plot")

    def set_tendencies(self):

        text = "  Mode : " + str(self.mode())

        if self.attribute in self.storage.table.attribute_levels:
            level = self.storage.table.attribute_levels[self.attribute]

            if constants.allows_order(level):
                text += "   Median : " + str(self.median())

            if constants.allows_mean(level):
                text += "   Mean : " + str(self.mean())

        self.infotext.SetLabel(text)

    def mode(self):

        return collections.Counter.most_common(self.counts)[0][0]

    def median(self):

        values = list()
        for i in self.values:
            for count in range(self.counts[i]):
                values.append(float(i))
        return statistics.median(values)

    def mean(self):

        values = list()
        for i in self.values:
            for count in range(self.counts[i]):
                values.append(float(i))
        return round(statistics.mean(values), 6)




