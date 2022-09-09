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

            values = list()
            for i in range(self.frame.main_grid.GetNumberRows()):
                value = self.frame.main_grid.GetCellValue(i, labelevent.GetCol())
                if value != "":
                    values.append(self.frame.main_grid.GetCellValue(i, labelevent.GetCol()))

            unique_values = list(set(values))
            unique_values.sort()

            if len(unique_values) == 0:
                return

            statistics_test = statistics.StatsPanel(self.frame.tabs, self.datastorage)
            statistics_test.load_histogram(unique_values, Counter(list(values)))
            self.frame.tabs.AddPage(statistics_test, "Stats")

        return add_stats
