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
from collections import Counter
import gettext

_ = gettext.gettext


class StatsPanel(wx.Panel):

    def __init__(self, panel, datastorage, menuservice, tableservice, statservice, attribute):
        wx.Panel.__init__(self, panel, -1)

        self.parent = panel
        self.storage = datastorage
        self.mservice = menuservice
        self.tservice = tableservice
        self.sservice = statservice

        self.attribute = attribute

        self.raw_data = None
        self.unique_values = None
        self.value_counts = None
        self.uncounted_values = None
        self.order_dict = None
        self.selection = 0

        self.figure = plt.figure()

        self.canvas = FigureCanvas(self, -1, self.figure)

        options = [_('Histogram'), _('Expanded Histogram'), _('Pie Chart'), _('Custom Order')]
        self.plot_combobox = wx.ComboBox(self, choices=options, style=wx.CB_READONLY)
        self.plot_combobox.SetSelection(0)

        sortings = [_('Alphabetical'), _('Numeric'), _('Substring'), _('Prefix'), _('Postfix'), _('Random')]
        self.order_combobox = wx.ComboBox(self, choices=sortings, style=wx.CB_READONLY)
        self.order_combobox.SetSelection(0)

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
        self.sort_text.SetLabel(_("Move Below Elements Into a Total Order:"))
        self.sort_text.Hide()
        self.sort_grid = grid.Grid(self)
        self.sort_grid.CreateGrid(0, 0)
        self.sort_grid.EnableDragColMove()
        self.sort_grid.HideRowLabels()
        self.sort_grid.Hide()
        self.sort_grid.Bind(grid.EVT_GRID_COL_MOVE, self.order_changed)

        self.hsizer_top = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer_top.Add(self.plot_combobox, 1, wx.TOP | wx.LEFT)
        self.hsizer_top.Add(self.infotext, 1, wx.TOP | wx.LEFT)
        self.hsizer_top.Add(self.binselector, 1, wx.TOP | wx.RIGHT)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.hsizer_top, 1, wx.TOP | wx.LEFT)
        self.sizer.Add(self.order_combobox, 1, wx.TOP | wx.LEFT)
        self.sizer.Add(self.canvas, 15, wx.TOP | wx.LEFT | wx.EXPAND)
        self.sizer.Add(self.sort_text, wx.TOP | wx.LEFT)
        self.sizer.Add(self.sort_grid, wx.TOP | wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        self.plot_combobox.Bind(wx.EVT_COMBOBOX, self.select_plot)
        self.order_combobox.Bind(wx.EVT_COMBOBOX, self.select_order)
        self.binselector.Bind(wx.EVT_TEXT, self.bin_change)

        self.Bind(wx.EVT_RIGHT_UP, self.onClick)
        self.sort_grid.Bind(wx.EVT_RIGHT_UP, self.onClick)
        self.canvas.Bind(wx.EVT_RIGHT_UP, self.onClick)

    def restore_raw(self):
        self.uncounted_values = self.raw_data
        self.unique_values = list(set(self.raw_data))
        self.value_counts = Counter(list(self.raw_data))

    def onClick(self, evt):
        evt.Skip()
        menu = wx.Menu()
        close = menu.Append(wx.ID_ANY, _("Close Tabs"))
        self.Bind(wx.EVT_MENU, self.close, close)
        if self.selection == 1 and self.unique_values and type(self.unique_values[0]) == float and self.attribute in self.sservice.datastorage.table.scalings:
            transfer = wx.Menu()
            nominal = transfer.Append(wx.ID_ANY, _("Nominal Scaling"))
            self.Bind(wx.EVT_MENU, self.get_transfer_to_scaling(constants.DIAGONAL), nominal)

            ordinal = transfer.Append(wx.ID_ANY, _("Ordinal Scaling"))
            self.Bind(wx.EVT_MENU, self.get_transfer_to_scaling(constants.ORDINAL), ordinal)

            interordinal = transfer.Append(wx.ID_ANY, _("Interordinal Scaling"))
            self.Bind(wx.EVT_MENU, self.get_transfer_to_scaling(constants.INTERORDINAL), interordinal)

            menu.Append(wx.ID_ANY, _("Transfer to Scaling"), transfer)
        self.PopupMenu(menu)
        menu.Destroy()

    def get_transfer_to_scaling(self, type):
        def transfer_to_scaling(evt=None):
            bins = min(int(self.binselector.GetLineText(0)), max(self.unique_values))
            bin_width = (max(self.unique_values) - min(self.unique_values)) / bins

            bin_ranges = list()
            for i in range(bins):
                bin_ranges.append((min(self.unique_values) + i*bin_width, min(self.unique_values) + (i+1)*bin_width))

            self.tservice.transfer_bins(self.attribute, bin_ranges, type)
        return transfer_to_scaling

    def close(self, evt=None):
        self.sservice.close_tab(self.attribute)

    def order_changed(self, evt):
        wx.CallAfter(self.update_order)

    def update_order(self):

        currently_numeric = type(self.unique_values[0]) == float

        new_order = list()
        order_dict = dict()
        for i in range(self.sort_grid.GetNumberCols()):
            if currently_numeric:
                new_order.append(float(self.sort_grid.GetColLabelValue(self.sort_grid.GetColAt(i))))
            else:
                new_order.append(self.sort_grid.GetColLabelValue(self.sort_grid.GetColAt(i)))

            order_dict[self.sort_grid.GetColLabelValue(self.sort_grid.GetColAt(i))] = i

        self.unique_values = new_order
        self.order_dict = order_dict

    def bin_change(self, evt=None):

        entry = self.binselector.GetLineText(0)
        if entry != "" and entry.isnumeric() and int(entry) > 0 and type(self.unique_values[0]) == float:
            bin_number = min(int(self.binselector.GetLineText(0)), max(self.unique_values))
            self.load_histplot(self.uncounted_values, bin_number)

    def order_numeric(self, evt=None):
        if self.isnumeric():
            self.restore_raw()
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
        self.restore_raw()
        unique_values_new = [str(i) for i in self.unique_values]
        self.unique_values = unique_values_new
        self.unique_values.sort()
        uncounted_values_new = [str(i) for i in self.uncounted_values]
        self.uncounted_values = uncounted_values_new
        value_counts_new = dict()
        for key in self.value_counts:
            value_counts_new[str(key)] = self.value_counts[key]
        self.value_counts = value_counts_new
        self.order_dict = None
        self.load_stats(self.selection)

    def order_random(self, evt=None):
        self.restore_raw()
        value_counts_new = dict()
        for key in self.value_counts:
            value_counts_new[str(key)] = self.value_counts[key]
        self.value_counts = value_counts_new
        random.shuffle(self.unique_values)
        self.reload_order_grid()
        self.update_order()
        self.load_stats(self.selection)

    def get_order_other(self, comparator, evt=None):
        def order_other(evt=None):
            self.restore_raw()
            unique_values_new = [str(i) for i in self.unique_values]
            self.unique_values = unique_values_new
            self.unique_values = constants.topological_sort(self.unique_values, comparator)
            uncounted_values_new = [str(i) for i in self.uncounted_values]
            self.uncounted_values = uncounted_values_new
            value_counts_new = dict()
            for key in self.value_counts:
                value_counts_new[str(key)] = self.value_counts[key]
            self.value_counts = value_counts_new
            self.reload_order_grid()
            self.update_order()
            self.load_stats(self.selection)
        return order_other

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

    def select_plot(self, evt):
        # Handle Selection via Combobox
        self.selection = evt.GetSelection()
        self.load_stats(evt.GetSelection())

    def select_order(self, evt):
        if evt.GetSelection() == 0:
            self.order_alphabetical()
        if evt.GetSelection() == 1:
            self.order_numeric()
        if evt.GetSelection() == 2:
            self.get_order_other(constants.substring)()
        if evt.GetSelection() == 3:
            self.get_order_other(constants.prefix)()
        if evt.GetSelection() == 4:
            self.get_order_other(constants.postfix)()
        if evt.GetSelection() == 5:
            self.order_random()

    def load_stats(self, selection):

        if not self.unique_values:
            self.infotext.SetLabel(_("No Statistics Available"))
            plt.figure(self.figure.number)
            plt.clf()
            self.figure.canvas.draw()
            return

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

        if not self.unique_values:
            return

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
                values.append(i)
        return values[math.ceil(len(values)/2) - 1]

    def mean(self):

        values = list()
        for i in self.unique_values:
            for count in range(self.value_counts[i]):
                values.append(float(i))
        return round(statistics.mean(values), 6)




