from collections import Counter

from scaling_app import statistics, tableservice


class Statservice:

    def __init__(self, frame, tableservice, datastorage):
        self.frame = frame
        self.tableservice = tableservice
        self.datastorage = datastorage
        self.menuservice = None

    def get_add_stats(self, col, attribute):
        def add_stats(evt=None):
            # Add Stats Header for Selected Attribute

            if attribute in self.datastorage.stats_visible:
                return

            self.tableservice.get_save_to_storage()()

            self.datastorage.stats_visible.add(attribute)

            # Restore Old Tab if Exists
            for tab in self.datastorage.stats:
                if tab.attribute == attribute:
                    self.frame.bottom_tabs.AddPage(tab, "Stats: " + attribute)
                    self.frame.bottom_tabs.SetSelection(self.frame.bottom_tabs.GetPageCount() - 1)
                    return

            unique_values, height, uncounted_values = self.compile_stats(col)

            if len(unique_values) == 0:
                return

            statistics_new = statistics.StatsPanel(self.frame.bottom_tabs, self.datastorage, self.menuservice, self.tableservice, self, attribute)
            self.datastorage.stats.append(statistics_new)

            statistics_new.uncounted_values = uncounted_values
            statistics_new.raw_data = uncounted_values
            statistics_new.load_histogram(unique_values, height)
            self.frame.bottom_tabs.AddPage(statistics_new, "Stats: " + attribute)
            self.frame.bottom_tabs.SetSelection(self.frame.bottom_tabs.GetPageCount() - 1)

        return add_stats

    def close_tab(self, attribute):
        # closes the current tab
        selection = self.frame.bottom_tabs.GetSelection()
        self.frame.bottom_tabs.SetSelection(selection - 1)
        self.frame.bottom_tabs.RemovePage(selection)
        self.datastorage.stats_visible.remove(attribute)
        print(self.datastorage.stats)

    def compile_stats(self, col):
        # Computes Unique Values and Respective Occurrence Counts from Selected Attribute
        values = list()
        for i in range(self.frame.many_valued_grid.GetNumberRows()):
            value = self.frame.many_valued_grid.GetCellValue(i, col)
            if value != "":
                values.append(self.frame.many_valued_grid.GetCellValue(i, col))

        unique_values = list(set(values))
        unique_values.sort()

        return unique_values, Counter(list(values)), values

    def update_all(self):
        # updates the stats for all attributes
        for stats in self.datastorage.stats:
            self.update_stats(attribute=stats.attribute)

    def update_stats(self, evt=None, attribute=None):

        # Should be Called with Either an Event or the Columns Attribute to Ascertain which Column is Affected

        # Ascertain Affected Column
        if attribute is None:
            attribute = self.frame.many_valued_grid.GetColLabelValue(evt.GetCol())

        affected_tab = None
        for stats_tab in self.datastorage.stats:
            if stats_tab.attribute == attribute:
                affected_tab = stats_tab

        currently_numeric = type(affected_tab.unique_values[0]) == float

        # Recompile all Values if Attribute was Input
        if evt is None:
            col = self.datastorage.table.col_labels.index(attribute)
            compiled_stats = self.compile_stats(col)
            affected_tab.unique_values = compiled_stats[0]
            affected_tab.value_counts = compiled_stats[1]
            affected_tab.uncounted_values = compiled_stats[2]
            affected_tab.raw_data = compiled_stats[2]
        else:
            compiled_stats = self.compile_stats(evt.GetCol())
            affected_tab.value_counts = compiled_stats[1]
            affected_tab.uncounted_values = compiled_stats[2]

            new_entry = self.frame.many_valued_grid.GetCellValue(evt.GetRow(), evt.GetCol())
            if len(affected_tab.unique_values) == 0:
                affected_tab.unique_values.append(str(new_entry))
            elif type(affected_tab.unique_values[0]) is str and new_entry not in affected_tab.unique_values:
                affected_tab.unique_values.append(str(new_entry))
            elif type(affected_tab.unique_values[0]) is float and float(new_entry) not in affected_tab.unique_values:
                affected_tab.unique_values.append(float(new_entry))
            affected_tab.raw_data = compiled_stats[2]

        # Reload Order Grid and Order Dictionary if it Exists
        if affected_tab.order_dict is not None:
            if affected_tab.sort_grid.GetNumberCols() > 0:
                tableservice.delete_cols(affected_tab.sort_grid)
            for i in range(len(affected_tab.unique_values)):
                affected_tab.sort_grid.AppendCols(1)
                affected_tab.sort_grid.SetColLabelValue(i, str(affected_tab.unique_values[i]))

            affected_tab.update_order()

        if currently_numeric:
            affected_tab.order_numeric()
        affected_tab.load_stats(affected_tab.selection)

    def clear_stats(self):
        # deletes the stats for all attributes
        self.datastorage.stats_visible.clear()
        self.datastorage.stats.clear()

        while self.frame.bottom_tabs.GetPageCount() > 3:
            self.frame.bottom_tabs.DeletePage(3)
