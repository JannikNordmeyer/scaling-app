from collections import Counter

from scaling_app import statistics, tableservice


class Statservice:

    def __init__(self, frame, tableservice, datastorage):
        self.frame = frame
        self.tableservice = tableservice
        self.datastorage = datastorage
        self.menuservice = None

    def get_add_stats(self, labelevent):
        def add_stats(evt=None):
            # Add Stats Header for Selected Attribute

            self.tableservice.get_save_to_storage()()
            attribute = (self.frame.main_grid.GetColLabelValue(labelevent.GetCol()))

            self.datastorage.stats_visible.add(attribute)

            # Restore Old Tab if Exists
            for tab in self.datastorage.stats:
                if tab.attribute == attribute:
                    self.frame.tabs.AddPage(tab, "Stats: " + attribute)
                    return

            unique_values, height, uncounted_values = self.compile_stats(labelevent.GetCol())

            if len(unique_values) == 0:
                return

            statistics_new = statistics.StatsPanel(self.frame.tabs, self.datastorage, self.menuservice, self.tableservice, self, attribute)
            self.datastorage.stats.append(statistics_new)

            statistics_new.uncounted_values = uncounted_values
            statistics_new.load_histogram(unique_values, height)
            self.frame.tabs.AddPage(statistics_new, "Stats: " + attribute)

        return add_stats

    def close_tab(self, attribute):
        selection = self.frame.tabs.GetSelection()
        self.frame.tabs.SetSelection(selection-1)
        self.frame.tabs.RemovePage(selection)
        self.datastorage.stats_visible.remove(attribute)
        print(self.datastorage.stats)

    def compile_stats(self, col):
        # Computes Unique Values and Respective Occurrence Counts from Selected Attribute
        values = list()
        for i in range(self.frame.main_grid.GetNumberRows()):
            value = self.frame.main_grid.GetCellValue(i, col)
            if value != "":
                values.append(self.frame.main_grid.GetCellValue(i, col))

        unique_values = list(set(values))
        unique_values.sort()

        return unique_values, Counter(list(values)), values

    def update_stats(self, evt=None, attribute=None):
        # Should be Called with Either an Event or the Columns Attribute to Ascertain which Column is Affected

        # Ascertain Affected Column
        if attribute is None:
            attribute = self.frame.main_grid.GetColLabelValue(evt.GetCol())

        affected_tab = None
        for stats_tab in self.datastorage.stats:
            if stats_tab.attribute == attribute:
                affected_tab = stats_tab

        # Recompile all Values if Attribute was Input
        if evt is None:
            col = self.datastorage.table.col_labels.index(attribute)
            affected_tab.unique_values, affected_tab.value_counts, affected_tab.uncounted_values = self.compile_stats(col)
        else:
            compiled_stats = self.compile_stats(evt.GetCol())
            affected_tab.value_counts = compiled_stats[1]
            affected_tab.uncounted_values = compiled_stats[2]

            new_entry = self.frame.main_grid.GetCellValue(evt.GetRow(), evt.GetCol())
            if len(affected_tab.unique_values) == 0:
                affected_tab.unique_values.append(str(new_entry))
            elif type(affected_tab.unique_values[0]) is str and new_entry not in affected_tab.unique_values:
                affected_tab.unique_values.append(str(new_entry))
            elif type(affected_tab.unique_values[0]) is float and float(new_entry) not in affected_tab.unique_values:
                affected_tab.unique_values.append(float(new_entry))

        # Reload Order Grid and Order Dictionary if it Exists
        if affected_tab.order_dict is not None:
            if affected_tab.sort_grid.GetNumberCols() > 0:
                tableservice.delete_cols(affected_tab.sort_grid)
            for i in range(len(affected_tab.unique_values)):
                affected_tab.sort_grid.AppendCols(1)
                affected_tab.sort_grid.SetColLabelValue(i, str(affected_tab.unique_values[i]))

            affected_tab.update_order()

        affected_tab.load_stats(affected_tab.selection)

    def clear_stats(self):
        self.datastorage.stats_visible.clear()
        self.datastorage.stats.clear()

        while self.frame.tabs.GetPageCount() > 3:
            self.frame.tabs.DeletePage(3)
