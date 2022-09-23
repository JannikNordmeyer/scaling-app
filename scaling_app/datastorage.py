
class Table:
    original = dict()
    col_labels = list()
    row_labels = list()
    scalings = dict()
    attribute_levels = dict()

    def set_scaling(self, attribute, row_labels, col_labels, table):
        self.scalings[attribute] = (row_labels, col_labels, table)

    def get_scaling(self, attribute):
        return self.scalings[attribute]


class DataStorage:
    lattice = None

    data = None
    table = Table()

    # Grid Tabs
    tabs = list()
    # Stat Tabs
    stats = list()

    # States
    edited = False
    result_visible = set()
    stats_visible = set()

    def set_edited(self, evt=None):
        self.edited = True

    def clear_edited(self, evt=None):
        self.edited = False

    def clear_table(self):
        self.table.original.clear()
        self.table.col_labels.clear()
        self.table.row_labels.clear()
        self.table.scalings.clear()
        main_grid = self.tabs[0]
        result_grid = self.tabs[1]
        self.tabs.clear()
        self.tabs.append(main_grid)
        self.tabs.append(result_grid)
        self.result_visible.clear()

    def status(self, evt=None):
        print("Status:")
        print("edited: " + str(self.edited))
        print("result_visible:" + str(self.result_visible))
        print("stats_visible:" + str(self.stats_visible))
        print("attribute levels" + str(self.table.attribute_levels))
        print("\n")
        print("tabs: " + str(self.tabs))
        print("scalings:")
        print(self.table.scalings)
        print("Table:")
        print(self.table.row_labels)
        print(self.table.col_labels)
        print(self.table.original)
        print("---------------------------------------")

