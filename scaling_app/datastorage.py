from scaling_app import constants


class Table:
    original = dict()
    col_labels = list()
    row_labels = list()
    scalings = dict()

    def set_scaling(self, attribute, row_labels, col_labels, table):
        self.scalings[attribute] = (row_labels, col_labels, table)

    def get_scaling(self, attribute):
        return self.scalings[attribute]


class DataStorage:
    lattice = None

    data = None
    table = Table()

    # States
    edited = False
    table_state = constants.ORIGINAL

    def set_edited(self, evt=None):
        self.edited = True

    def clear_edited(self, evt=None):
        self.edited = False
