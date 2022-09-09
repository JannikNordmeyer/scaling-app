from collections import Counter

from scaling_app import statistics


class Statservice:

    def __init__(self, frame, tableservice, datastorage):
        self.frame = frame
        self.tableservice = tableservice
        self.datastorage = datastorage

    def get_add_stats(self, labelevent):
        def add_stats(evt=None):

            self.tableservice.get_save_to_storage()()

            unique_values, height = self.compile_stats(labelevent.GetCol())

            if len(unique_values) == 0:
                return
            attribute = (self.frame.main_grid.GetColLabelValue(labelevent.GetCol()))

            self.datastorage.stats_visible.add(attribute)

            statistics_new = statistics.StatsPanel(self.frame.tabs, self.datastorage, attribute)
            self.datastorage.stats.append(statistics_new)

            statistics_new.load_histogram(unique_values, height)
            self.frame.tabs.AddPage(statistics_new, "Stats: " + attribute)

        return add_stats

    def compile_stats(self, col):
        values = list()
        for i in range(self.frame.main_grid.GetNumberRows()):
            value = self.frame.main_grid.GetCellValue(i, col)
            if value != "":
                values.append(self.frame.main_grid.GetCellValue(i, col))

        unique_values = list(set(values))
        unique_values.sort()

        return unique_values, Counter(list(values))

    def update_stats(self):

        for stats in self.datastorage.stats:

            attribute = stats.attribute
            col = self.datastorage.table.col_labels.index(attribute)

            stats.values, stats.counts = self.compile_stats(col)
            stats.load_stats(stats.selection)

    def clear_stats(self):
        self.datastorage.stats_visible.clear()
        self.datastorage.stats.clear()

        while self.frame.tabs.GetPageCount() > 2:
            self.frame.tabs.DeletePage(2)
