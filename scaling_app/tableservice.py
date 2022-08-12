import csv
import wx
import wx.grid as grid
from scaling_app import constants


class TableService:

    def __init__(self, frame, datastorage):
        self.frame = frame
        self.datastorage = datastorage

    def fill_table(self):

        values = csv.reader(self.datastorage.data, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)

        self.frame.grid.DeleteRows(0, self.frame.grid.GetNumberRows())
        self.frame.grid.DeleteCols(0, self.frame.grid.GetNumberCols())
        self.frame.grid.AppendRows(values.line_num)

        rowlabellength = 0
        for row in values:

            if values.line_num == 1:
                rowlabellength = len(row)
                self.frame.grid.AppendCols(len(row))
                i = 0
                for entry in row:
                    self.frame.grid.SetColLabelValue(i, entry)
                    i += 1
            else:
                self.frame.grid.AppendRows(1)
                self.frame.grid.SetRowLabelValue(values.line_num - 2, str(values.line_num - 1))
                j = 0
                first = True
                for entry in row:
                    if len(row) == rowlabellength + 1 and first:
                        self.frame.grid.SetRowLabelValue(values.line_num - 2, entry)
                        first = False
                        continue
                    self.frame.grid.SetCellValue(values.line_num - 2, j, entry)
                    j += 1
        self.frame.grid.SetRowLabelSize(grid.GRID_AUTOSIZE)
        self.frame.grid.SetCornerLabelValue("")

    def get_to_scaling(self, labelevent, type):
        def to_scaling(evt):

            if self.frame.grid.GetColLabelValue(labelevent.GetCol()) in self.datastorage.table.scalings:
                self.load_from_storage(self.frame.grid.GetColLabelValue(labelevent.GetCol()))
                return

            self.save_to_storage(labelevent)
            self.frame.grid.DeleteCols(0, self.frame.grid.GetNumberCols())
            self.frame.grid.SetCornerLabelValue(self.datastorage.table.col_labels[labelevent.GetCol()])

            if type == constants.EMPTY:
                self.frame.grid.AppendCols(1)
                self.frame.grid.SetColLabelValue(0, self.datastorage.table.col_labels[labelevent.GetCol()])
                for i in range(self.frame.grid.GetNumberRows()):
                    self.frame.grid.SetCellValue(i, 0, self.datastorage.table.original[i, labelevent.GetCol()])

            self.datastorage.table_state = constants.SCALING

        return to_scaling

    def return_to_original(self, evt=None):
        self.save_to_storage()
        self.load_from_storage(constants.ORIGINAL)

    def save_to_storage(self, evt=None):
        # Save Original Table
        if self.datastorage.table_state == constants.ORIGINAL:
            self.datastorage.table.col_labels.clear()
            self.datastorage.table.row_labels.clear()
            self.datastorage.table.original.clear()

            for a in range(self.frame.grid.GetNumberCols()):
                self.datastorage.table.col_labels.append(self.frame.grid.GetColLabelValue(a))
            for b in range(self.frame.grid.GetNumberRows()):
                self.datastorage.table.row_labels.append(self.frame.grid.GetRowLabelValue(b))

            for i in range(self.frame.grid.GetNumberRows()):
                for j in range(self.frame.grid.GetNumberCols()):
                    self.datastorage.table.original[(i, j)] = self.frame.grid.GetCellValue(i, j)

        # Save Current Scaling
        if self.datastorage.table_state == constants.SCALING:

            row_labels = list()
            col_labels = list()
            for a in range(self.frame.grid.GetNumberRows()):
                row_labels.append(self.frame.grid.GetRowLabelValue(a))
            for b in range(self.frame.grid.GetNumberCols()):
                col_labels.append(self.frame.grid.GetColLabelValue(b))

            table = dict()
            for i in range(self.frame.grid.GetNumberRows()):
                for j in range(self.frame.grid.GetNumberCols()):
                    table[(i, j)] = self.frame.grid.GetCellValue(i, j)

            self.datastorage.table.set_scaling(self.frame.grid.GetCornerLabelValue(), row_labels, col_labels, table)

    def load_from_storage(self, target):

        self.frame.grid.DeleteRows(0, self.frame.grid.GetNumberRows())
        self.frame.grid.DeleteCols(0, self.frame.grid.GetNumberCols())

        # Load Original
        if target == constants.ORIGINAL:

            self.frame.grid.AppendCols(len(self.datastorage.table.col_labels))
            for a in range(len(self.datastorage.table.col_labels)):
                self.frame.grid.SetColLabelValue(a, self.datastorage.table.col_labels[a])
            self.frame.grid.AppendRows(len(self.datastorage.table.row_labels))
            for b in range(len(self.datastorage.table.row_labels)):
                self.frame.grid.SetRowLabelValue(b, self.datastorage.table.row_labels[b])
            for coords, value in self.datastorage.table.original.items():
                self.frame.grid.SetCellValue(coords[0], coords[1], value)
            self.frame.grid.SetCornerLabelValue("")
            self.datastorage.table_state = constants.ORIGINAL
            return

        # Load Existing Scaling
        scaling = self.datastorage.table.scalings[target]
        row_labels = scaling[0]
        col_labels = scaling[1]
        table = scaling[2]

        self.frame.grid.AppendCols(len(col_labels))
        for a in range(len(col_labels)):
            self.frame.grid.SetColLabelValue(a, col_labels[a])
        self.frame.grid.AppendRows(len(row_labels))
        for a in range(len(row_labels)):
            self.frame.grid.SetRowLabelValue(a, row_labels[a])
        for coords, value in table.items():
            self.frame.grid.SetCellValue(coords[0], coords[1], value)
        self.frame.grid.SetCornerLabelValue(target)
        self.datastorage.table_state = constants.SCALING




    def get_delete_row(self, labelevent):
        def delete_row(evt):
            for i in range(self.frame.grid.GetNumberRows() - labelevent.GetRow()):
                self.frame.grid.SetRowLabelValue(labelevent.GetRow() + i, self.frame.grid.GetRowLabelValue(labelevent.GetRow() + i + 1))
            self.frame.grid.DeleteRows(pos=labelevent.GetRow())
            self.datastorage.edited = True

        return delete_row

    def get_purge_row(self, labelevent):
        def purge_row(evt):
            if not self.is_empty():
                self.datastorage.edited = True
            for i in range(self.frame.grid.GetNumberCols()):
                self.frame.grid.SetCellValue(labelevent.GetRow(), i, "")

        return purge_row

    def get_edit_row_label(self, labelevent):
        def edit_row_label(evt):
            dialog = wx.TextEntryDialog(None, "Row name:", caption="New Row", value="",
                                        style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
            dialog.ShowModal()
            name = dialog.GetValue()
            dialog.Destroy()
            if name != "":
                self.frame.grid.SetRowLabelValue(labelevent.GetRow(), name)
                self.datastorage.set_edited()

        return edit_row_label

    def get_add_row(self, labelevent):
        def add_row(evt):
            self.frame.grid.AppendRows()
            self.cascade_row(labelevent.GetRow())
            self.frame.grid.SetRowLabelValue(labelevent.GetRow()+1, "")
            self.datastorage.set_edited()

        return add_row

    def get_delete_col(self, labelevent):
        def delete_col(evt):
            self.frame.grid.DeleteCols(pos=labelevent.GetCol(), updateLabels=False)
            self.datastorage.set_edited()

        return delete_col

    def get_purge_col(self, labelevent):
        def purge_col(evt):
            if not self.is_empty():
                self.datastorage.set_edited()
            for i in range(self.frame.grid.GetNumberRows()):
                self.frame.grid.SetCellValue(i, labelevent.GetCol(), "")

        return purge_col

    def get_edit_col_label(self, labelevent):
        def edit_col_label(evt):
            dialog = wx.TextEntryDialog(None, "Column name:", caption="New Column", value="",
                                        style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
            dialog.ShowModal()
            name = dialog.GetValue()
            dialog.Destroy()
            if name != "":
                self.frame.grid.SetColLabelValue(labelevent.GetCol(), name)
                self.datastorage.set_edited()

        return edit_col_label

    def get_add_col(self, labelevent):
        def add_col(evt):
            dialog = wx.TextEntryDialog(None, "Column name:", caption="New Column", value="",
                                        style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
            dialog.ShowModal()
            name = dialog.GetValue()
            dialog.Destroy()
            if name != "":
                self.frame.grid.AppendCols()
                self.frame.grid.SetColLabelValue(self.frame.grid.GetNumberCols()-1, name)
                self.cascade_col(labelevent.GetCol())
                self.datastorage.set_edited()

        return add_col

    def cascade_row(self, pos):
        number_rows = self.frame.grid.GetNumberRows()
        i = 0
        while i < number_rows - pos - 2:
            self.swap_row(number_rows - 2 - i, number_rows - 1 - i)
            i += 1

    def swap_row(self, a, b):

        temp = self.frame.grid.GetRowLabelValue(a)
        self.frame.grid.SetRowLabelValue(a, self.frame.grid.GetRowLabelValue(b))
        self.frame.grid.SetRowLabelValue(b, temp)
        for i in range(self.frame.grid.GetNumberCols()):

            temp = self.frame.grid.GetCellValue(a, i)
            self.frame.grid.SetCellValue(a, i, self.frame.grid.GetCellValue(b, i))
            self.frame.grid.SetCellValue(b, i, temp)

    def cascade_col(self, pos):
        number_cols = self.frame.grid.GetNumberCols()
        i = 0
        while i < number_cols - pos - 2:
            self.swap_col(number_cols - 2 - i, number_cols - 1 - i)
            i += 1

    def swap_col(self, a, b):

        temp = self.frame.grid.GetColLabelValue(a)
        self.frame.grid.SetColLabelValue(a, self.frame.grid.GetColLabelValue(b))
        self.frame.grid.SetColLabelValue(b, temp)
        for i in range(self.frame.grid.GetNumberRows()):

            temp = self.frame.grid.GetCellValue(i, a)
            self.frame.grid.SetCellValue(i, a, self.frame.grid.GetCellValue(i, b))
            self.frame.grid.SetCellValue(i, b, temp)

    def purge_table(self, evt):
        if not self.is_empty():
            self.datastorage.set_edited()
            self.frame.grid.ClearGrid()

    def reset_table(self, evt=None):

        self.frame.grid.DeleteRows(0, self.frame.grid.GetNumberRows())
        self.frame.grid.DeleteCols(0, self.frame.grid.GetNumberCols())
        self.frame.grid.AppendRows(16)
        self.frame.grid.AppendCols(8)
        for i in range(self.frame.grid.GetNumberRows()):
            self.frame.grid.SetRowLabelValue(i, str(i+1))

    def is_empty(self):
        for i in range(self.frame.grid.GetNumberRows()):
            for j in range(self.frame.grid.GetNumberCols()):
                if self.frame.grid.GetCellValue(i, j) != "":
                    return False
        return True

