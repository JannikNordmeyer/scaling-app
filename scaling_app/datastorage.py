from scaling_app import constants


class Table:
    original = dict()
    col_labels = list()
    row_labels = list()
    scalings = dict()

    def set_scaling(self, attribute, row_labels, col_labels, table, data_type):
        self.scalings[attribute] = (row_labels, col_labels, table, data_type)

    def get_scaling(self, attribute):
        return self.scalings[attribute]


class DataStorage:
    lattice = None

    data = None
    table = Table()

    # States
    edited = False
    table_state = constants.ORIGINAL
    expanded_cols = list()
    scaling_type = None

    def set_edited(self, evt=None):
        self.edited = True

    def clear_edited(self, evt=None):
        self.edited = False

    def clear_table(self):
        self.table.original.clear()
        self.table.col_labels.clear()
        self.table.row_labels.clear()
        self.table.scalings.clear()

