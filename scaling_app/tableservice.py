import csv
import wx
import wx.grid as grid


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


    def reset_table(self, evt):

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

