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

            unique_values, height, uncounted_values = self.compile_stats(labelevent.GetCol())

            if len(unique_values) == 0:
                return
            attribute = (self.frame.main_grid.GetColLabelValue(labelevent.GetCol()))

            self.datastorage.stats_visible.add(attribute)

            statistics_new = statistics.StatsPanel(self.frame.tabs, self.datastorage, self.menuservice, self.tableservice, self, attribute)
            self.datastorage.stats.append(statistics_new)

            statistics_new.uncounted_values = uncounted_values
            statistics_new.load_histogram(unique_values, height)
            self.frame.tabs.AddPage(statistics_new, "Stats: " + attribute)

        return add_stats

    def close_tab(self, evt=None):
        selection = self.frame.tabs.GetSelection()
        self.frame.tabs.SetSelection(selection-1)
        self.frame.tabs.DeletePage(selection)

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

    def update_stats(self):
        # Recompiles and Display Stats for each Stats Header

        for stats_tab in self.datastorage.stats:

            attribute = stats_tab.attribute
            col = self.datastorage.table.col_labels.index(attribute)

            stats_tab.unique_values, stats_tab.value_counts, stats_tab.uncounted_values = self.compile_stats(col)

            # Reload Order Grid and Order Dictionary if it Exists
            if stats_tab.order_dict is not None:
                if stats_tab.sort_grid.GetNumberCols() > 0:
                    tableservice.delete_cols(stats_tab.sort_grid)
                for i in range(len(stats_tab.unique_values)):
                    stats_tab.sort_grid.AppendCols(1)
                    stats_tab.sort_grid.SetColLabelValue(i, str(stats_tab.unique_values[i]))

                stats_tab.update_order()

            stats_tab.load_stats(stats_tab.selection)

    def clear_stats(self):
        self.datastorage.stats_visible.clear()
        self.datastorage.stats.clear()

        while self.frame.tabs.GetPageCount() > 3:
            self.frame.tabs.DeletePage(3)
