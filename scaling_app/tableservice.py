import csv
import wx


class TableService:

    def __init__(self, frame, datastorage):
        self.frame = frame
        self.datastorage = datastorage

    def fill_table(self):

        values = csv.reader(self.datastorage.data, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)

        self.frame.grid.DeleteRows(0, self.frame.grid.GetNumberRows())
        self.frame.grid.DeleteCols(0, self.frame.grid.GetNumberCols())
        self.frame.grid.AppendRows(values.line_num)

        for row in values:

            if values.line_num == 1:
                self.frame.grid.AppendCols(len(row))
                i = 0
                for entry in row:
                    self.frame.grid.SetColLabelValue(i, entry)
                    i += 1
            else:
                self.frame.grid.AppendRows(1)
                j = 0
                for entry in row:
                    self.frame.grid.SetCellValue(values.line_num - 2, j, entry)
                    j += 1

    def get_delete_row(self, labelevent):
        def delete_row(evt):
            self.frame.grid.DeleteRows(pos=labelevent.GetRow(), updateLabels=False)

        return delete_row

    def get_clear_row(self, labelevent):
        def clear_row(evt):
            for i in range(self.frame.grid.GetNumberCols()):
                self.frame.grid.SetCellValue(labelevent.GetRow(), i, "")

        return clear_row

    def get_add_row(self, labelevent):
        def add_row(evt):
            self.frame.grid.AppendRows()
            self.cascade_row(labelevent.GetRow())

        return add_row

    def get_delete_col(self, labelevent):
        def delete_col(evt):
            self.frame.grid.DeleteCols(pos=labelevent.GetCol(), updateLabels=False)

        return delete_col

    def get_clear_col(self, labelevent):
        def clear_col(evt):
            for i in range(self.frame.grid.GetNumberRows()):
                self.frame.grid.SetCellValue(i, labelevent.GetCol(), "")

        return clear_col

    def get_edit_label(self, labelevent):
        def edit_label(evt):
            dialog = wx.TextEntryDialog(None, "Column name:", caption="New Column", value="",
                                        style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
            dialog.ShowModal()
            name = dialog.GetValue()
            dialog.Destroy()
            if name != "":
                self.frame.grid.SetColLabelValue(labelevent.GetCol(), name)

        return edit_label

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

        return add_col

    def cascade_row(self, pos):
        number_rows = self.frame.grid.GetNumberRows()
        i = 0
        while i < number_rows - pos - 2:
            self.swap_row(number_rows - 2 - i, number_rows - 1 - i)
            i += 1

    def swap_row(self, a, b):
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

    def clear_table(self, evt):
        for i in range(self.frame.grid.GetNumberRows()):
            for j in range(self.frame.grid.GetNumberCols()):
                self.frame.grid.SetCellValue(i, j, "")

    def reset_table(self, evt):
        self.frame.grid.DeleteRows(0, self.frame.grid.GetNumberRows())
        self.frame.grid.DeleteCols(0, self.frame.grid.GetNumberCols())
        self.frame.grid.AppendRows(16)
        self.frame.grid.AppendCols(8)
