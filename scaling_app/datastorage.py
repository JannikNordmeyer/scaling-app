
class Table:
    # table to hold main formal context and scalings
    original = dict()
    col_labels = list()
    row_labels = list()
    scalings = dict()
    attribute_levels = dict()

    def set_scaling(self, attribute, row_labels, col_labels, table):
        # Adds scaling to specified attribute
        self.scalings[attribute] = (row_labels, col_labels, table)

    def get_scaling(self, attribute):
        # returns the scaling of the specified attribute
        return self.scalings[attribute]


class DataStorage:
    lattice = None

    data = None
    table = Table()

    concepts_tab = None
    implications_tab = None
    rules_tab = None

    # Grid Tabs
    grid_tabs = list()
    # Stat Tabs
    stats = list()

    # States
    edited = False
    result_visible = set()
    stats_visible = set()

    def set_edited(self, evt=None):
        # Sets edited flag
        self.edited = True

    def clear_edited(self, evt=None):
        # removes edited flag
        self.edited = False

    def clear_table(self):
        # clears main context and removes associated data
        self.table.original.clear()
        self.table.col_labels.clear()
        self.table.row_labels.clear()
        self.table.scalings.clear()
        main_grid = self.grid_tabs[0]
        result_grid = self.grid_tabs[1]
        self.grid_tabs.clear()
        self.grid_tabs.append(main_grid)
        self.grid_tabs.append(result_grid)
        self.result_visible.clear()

    def status(self, evt=None):
        print("Status:")
        print("edited: " + str(self.edited))
        print("result_visible:" + str(self.result_visible))
        print("stats_visible:" + str(self.stats_visible))
        print("attribute levels" + str(self.table.attribute_levels))
        print("\n")
        print("tabs: " + str(self.grid_tabs))
        print("scalings:")
        print(self.table.scalings)
        print("Table:")
        print(self.table.row_labels)
        print(self.table.col_labels)
        print(self.table.original)
        print("---------------------------------------")

