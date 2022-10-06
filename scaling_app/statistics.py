import collections
import math
import random
import statistics
import seaborn as sns
import wx
import wx.grid as grid
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from scaling_app import constants, tableservice


class StatsPanel(wx.Panel):

    def __init__(self, panel, datastorage, menuservice, tableservice, statservice, attribute):
        wx.Panel.__init__(self, panel, -1)

        self.parent = panel
        self.storage = datastorage
        self.mservice = menuservice
        self.tservice = tableservice
        self.sservice = statservice

        self.attribute = attribute

        self.is_numeric = False
        self.unique_values = None
        self.value_counts = None
        self.uncounted_values = None
        self.order_dict = None
        self.selection = 0

        self.figure = plt.figure()

        self.canvas = FigureCanvas(self, -1, self.figure)

        options = ['Histogram', 'Expanded Histogram', 'Pie Chart', 'Custom Order']
        self.combobox = wx.ComboBox(self, choices=options, style=wx.CB_READONLY)
        self.combobox.SetSelection(0)

        # Text for Central Tendencies
        self.infotext = wx.StaticText(self)
        font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.infotext.SetFont(font)
        self.infotext.SetLabel("")

        # Text Control for Bin Amount
        self.binselector = wx.TextCtrl(self, size=wx.Size(1, 25))
        self.binselector.Hide()

        # Pseudogrid for Set Ordering
        self.sort_text = wx.StaticText(self)
        self.sort_text.SetLabel("Move Below Elements Into a Total Order:")
        self.sort_text.Hide()
        self.sort_grid = grid.Grid(self)
        self.sort_grid.CreateGrid(0, 0)
        self.sort_grid.EnableDragColMove()
        self.sort_grid.HideRowLabels()
        self.sort_grid.Hide()
        self.sort_grid.Bind(grid.EVT_GRID_COL_MOVE, self.order_changed)

        self.hsizer_top = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer_top.Add(self.combobox, 1, wx.TOP | wx.LEFT)
        self.hsizer_top.Add(self.infotext, 1, wx.TOP | wx.LEFT)
        self.hsizer_top.Add(self.binselector, 1, wx.TOP | wx.RIGHT)

        # Sorting Option Buttons
        self.button_numeric = wx.Button(self)
        self.button_numeric.SetLabel("Numeric")
        self.button_numeric.Bind(wx.EVT_BUTTON, self.order_numeric)
        self.button_alphabetical = wx.Button(self)
        self.button_alphabetical.SetLabel("Alphabetical")
        self.button_alphabetical.Bind(wx.EVT_BUTTON, self.order_alphabetical)
        self.button_random = wx.Button(self)
        self.button_random.SetLabel("Random")
        self.hsizer_bot = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer_bot.Add(self.button_numeric, 1, wx.TOP | wx.LEFT)
        self.hsizer_bot.Add(self.button_alphabetical, 1, wx.TOP | wx.LEFT)
        self.hsizer_bot.Add(self.button_random, 1, wx.TOP | wx.LEFT)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.hsizer_top, 1, wx.TOP | wx.LEFT)
        self.sizer.Add(self.canvas, 15, wx.TOP | wx.LEFT | wx.EXPAND)
        self.sizer.Add(self.sort_text, wx.TOP | wx.LEFT)
        self.sizer.Add(self.sort_grid, wx.TOP | wx.LEFT | wx.EXPAND)
        self.sizer.Add(self.hsizer_bot, 1, wx.TOP | wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        self.combobox.Bind(wx.EVT_COMBOBOX, self.select)
        self.binselector.Bind(wx.EVT_TEXT, self.bin_change)

    def order_changed(self, evt):
        wx.CallAfter(self.update_order)

    def update_order(self):

        new_order = list()
        order_dict = dict()
        for i in range(self.sort_grid.GetNumberCols()):
            new_order.append(self.sort_grid.GetColLabelValue(self.sort_grid.GetColAt(i)))

            order_dict[self.sort_grid.GetColLabelValue(self.sort_grid.GetColAt(i))] = i

        self.unique_values = new_order
        self.order_dict = order_dict

    def bin_change(self, evt=None):

        entry = self.binselector.GetLineText(0)
        if entry != "" and entry.isnumeric() and int(entry) > 0:
            bin_number = min(int(self.binselector.GetLineText(0)), len(self.unique_values))
            self.load_histplot(self.uncounted_values, bin_number)

    def order_numeric(self, evt=None):
        if self.isnumeric():
            self.sservice.update_stats()
            unique_values_new = [float(i) for i in self.unique_values]
            self.unique_values = unique_values_new
            self.unique_values.sort(key=float)
            uncounted_values_new = [float(i) for i in self.uncounted_values]
            self.uncounted_values = uncounted_values_new
            self.uncounted_values.sort(key=float)
            value_counts_new = dict()
            for key in self.value_counts:
                value_counts_new[float(key)] = self.value_counts[key]
            self.value_counts = value_counts_new
            self.order_dict = None
            self.load_stats(self.selection)

    def order_alphabetical(self, evt=None):
        self.sservice.update_stats()
        unique_values_new = [str(i) for i in self.unique_values]
        self.unique_values = unique_values_new
        self.unique_values.sort()
        uncounted_values_new = [str(i) for i in self.uncounted_values]
        self.uncounted_values = uncounted_values_new
        self.uncounted_values.sort()
        value_counts_new = dict()
        for key in self.value_counts:
            value_counts_new[str(key)] = self.value_counts[key]
        self.value_counts = value_counts_new
        self.order_dict = None
        self.load_stats(self.selection)

    def order_random(self, evt=None):
        pass

    def isnumeric(self):
        numeric = True
        for value in self.unique_values:
            try:
                float(value)
            except:
                numeric = False
                break
        return numeric

    def load_order(self):
        self.binselector.Hide()
        self.infotext.Hide()
        self.sort_grid.Hide()
        self.canvas.Hide()
        self.sort_text.Show()
        self.sort_grid.Show()
        self.reload_order_grid()

    def reload_order_grid(self):
        if self.sort_grid.GetNumberCols() > 0:
            tableservice.delete_cols(self.sort_grid)
        for i in range(len(self.unique_values)):
            self.sort_grid.AppendCols(1)
            self.sort_grid.SetColLabelValue(i, str(self.unique_values[i]))

    def select(self, evt):
        # Handle Selection via Combobox
        self.selection = evt.GetSelection()
        self.load_stats(evt.GetSelection())

    def load_stats(self, selection):

        if selection == 0:
            self.load_histogram(self.unique_values, self.value_counts)
        if selection == 1:
            self.load_histplot(self.uncounted_values, len(self.unique_values))
        if selection == 2:
            self.load_pie(self.unique_values, self.value_counts)
        if selection == 3:
            self.load_order()

        self.Layout()

    def load_histogram(self, values, counts):

        plt.figure(self.figure.number)
        plt.clf()

        height = list()
        for value in values:
            height.append(counts[value])
        self.unique_values = values
        self.value_counts = counts

        sns.set(style="darkgrid")
        sns.barplot(x=values, y=height, order=self.unique_values)

        self.set_tendencies()
        self.binselector.Hide()
        self.sort_text.Hide()
        self.sort_grid.Hide()
        self.infotext.Show()
        self.canvas.Show()
        self.figure.canvas.draw()

    def load_histplot(self, uncounted_values, bins=None):
        plt.figure(self.figure.number)
        plt.clf()

        print(uncounted_values)
        if self.order_dict is not None:
            uncounted_values.sort(key=lambda val: self.order_dict[str(val)])
            for i in range(len(uncounted_values)):
                uncounted_values[i] = str(uncounted_values[i])
        else:
            uncounted_values.sort()

        sns.set(style="darkgrid")
        sns.histplot(data=uncounted_values, bins=bins)

        self.set_tendencies()
        label = self.infotext.GetLabel()
        if not label.endswith("       Bins:  "):
            self.infotext.SetLabel(label + "       Bins:  ")
        self.binselector.Show()
        self.infotext.Show()
        self.sort_text.Hide()
        self.sort_grid.Hide()
        self.canvas.Show()
        self.figure.canvas.draw()

    def load_pie(self, values, counts):

        plt.figure(self.figure.number)
        plt.clf()

        height = list()
        for value in values:
            height.append(counts[value])
        self.unique_values = values
        self.value_counts = counts

        plt.pie(height, labels=values, autopct='%1.1f%%',
                shadow=True, startangle=90)

        self.set_tendencies()
        self.binselector.Hide()
        self.sort_text.Hide()
        self.sort_grid.Hide()
        self.infotext.Show()
        self.canvas.Show()
        self.figure.canvas.draw()

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

        return collections.Counter.most_common(self.value_counts)[0][0]

    def median(self):

        values = list()
        for i in self.unique_values:
            for count in range(self.value_counts[i]):
                values.append(float(i))
        return values[math.ceil(len(values)/2) - 1]

    def mean(self):

        values = list()
        for i in self.unique_values:
            for count in range(self.value_counts[i]):
                values.append(float(i))
        return round(statistics.mean(values), 6)




