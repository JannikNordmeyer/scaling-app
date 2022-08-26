import csv
import wx
import wx.grid as grid
from scaling_app import constants


class TableService:

    def __init__(self, frame, datastorage):
        self.frame = frame
        self.datastorage = datastorage
        self.mservice = None

        self.current_grid = None

    def fill_table(self):

        self.current_grid = self.frame.grid

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

    def load_expanded(self, evt=None):

        for i in range(len(self.datastorage.table.col_labels), -1, -1):
            self.get_expand_column(i)()

        self.datastorage.expanded = True

    def get_expand_column(self, col):
        def expand_column(evt=None):
            if not self.datastorage.expanded:
                self.get_save_to_storage(0)()
            if self.frame.grid.GetColLabelValue(col) not in self.datastorage.table.scalings:
                return
            scaling = self.datastorage.table.scalings[self.frame.grid.GetColLabelValue(col)]
            col_labels = scaling[1]
            scaling_table = scaling[2]
            scaling_type = scaling[3]

            col_offset = self.frame.grid.GetNumberCols()
            self.frame.grid.AppendCols(len(col_labels))
            for new_col in range(len(col_labels)):
                self.frame.grid.SetColLabelValue(col_offset + new_col, self.frame.grid.GetColLabelValue(col) + "\n" + col_labels[new_col])
            if scaling_type == constants.INT:
                for i in range(self.frame.grid.GetNumberRows()):
                    if self.frame.grid.GetCellValue(i, col) != "":
                        value = int(self.frame.grid.GetCellValue(i, col))
                        for j in range(len(col_labels)):
                            self.frame.grid.SetCellValue(i, col_offset+j, scaling_table[(value, j)])
            if scaling_type == constants.GENERIC:
                for i in range(self.frame.grid.GetNumberRows()):
                    if self.frame.grid.GetCellValue(i, col) != "":
                        value = self.frame.grid.GetCellValue(i, col)
                        for j in range(len(col_labels)):
                            self.frame.grid.SetCellValue(i, col_offset+j, scaling_table[(col_labels.index(value), j)])
            for i in range(len(col_labels)):
                self.cascade_col(col)
            self.frame.grid.DeleteCols(col)
            self.datastorage.expanded = True
            if self.frame.grid.GetColLabelValue(col).split("\n", 1)[0] not in self.datastorage.expanded_cols:
                self.datastorage.expanded_cols.append(self.frame.grid.GetColLabelValue(col).split("\n", 1)[0])

        return expand_column

    def get_unexpand_column(self, col):
        def unexpand_column(evt=None):

            self.current_grid = self.datastorage.tabs[self.frame.csvtabs.GetSelection()]
            attribute = self.frame.grid.GetColLabelValue(col).split("\n", 1)[0]
            self.load_from_storage(constants.ORIGINAL)

            self.datastorage.expanded_cols.remove(attribute)

            still_expanded = False
            for i in range(self.frame.grid.GetNumberCols()):
                if self.frame.grid.GetColLabelValue(i) in self.datastorage.expanded_cols:
                    still_expanded = True
                    self.get_expand_column(i)()
            if not still_expanded:
                self.datastorage.expanded = False

        return unexpand_column

    def get_to_scaling(self, labelevent, type):
        def to_scaling(evt):

            # load from storage if scaling exists and right tab is selected
            if self.current_grid.GetCornerLabelValue() in self.datastorage.table.scalings:
                self.load_from_storage(self.current_grid.GetCornerLabelValue())
                return

            self.get_save_to_storage(self.frame.csvtabs.GetSelection())()

            self.new_tab(self.frame.grid.GetColLabelValue(labelevent.GetCol()))
            self.current_grid.SetCornerLabelValue(self.datastorage.table.col_labels[labelevent.GetCol()])

            if type == constants.EMPTY or type == constants.DICHOTOM:
                values = list()
                for i in range(self.frame.grid.GetNumberRows()):
                    if self.frame.grid.GetCellValue(i, labelevent.GetCol()) not in values:
                        if self.frame.grid.GetCellValue(i, labelevent.GetCol()) != "":
                            values.append(self.frame.grid.GetCellValue(i, labelevent.GetCol()))
                self.current_grid.DeleteCols(0, self.current_grid.GetNumberCols())
                self.current_grid.DeleteRows(0, self.current_grid.GetNumberRows())
                self.current_grid.AppendCols(len(values))
                self.current_grid.AppendRows(len(values))
                for i in range(self.current_grid.GetNumberRows()):
                    self.current_grid.SetColLabelValue(i, values[i])
                    self.current_grid.SetRowLabelValue(i, values[i])
                    if type == constants.DICHOTOM:
                        self.current_grid.SetCellValue(i, i, "✘")
                self.datastorage.scaling_type = constants.GENERIC

            if type == constants.DIAGONAL or type == constants.ORDINAL:
                max_value = self.check_int_col(labelevent.GetCol())
                self.current_grid.DeleteCols(0, self.current_grid.GetNumberCols())
                self.current_grid.AppendCols(max_value+1)
                self.current_grid.DeleteRows(0, self.frame.grid.GetNumberRows())
                self.current_grid.AppendRows(max_value+1)
                for a in range(max_value+1):
                    self.current_grid.SetColLabelValue(a, str(a))
                    self.current_grid.SetRowLabelValue(a, str(a))
                for i in range(self.current_grid.GetNumberRows()):
                    row_value = self.current_grid.GetRowLabelValue(i)
                    for j in range(self.current_grid.GetNumberCols()):
                        col_value = self.current_grid.GetColLabelValue(j)
                        if type == constants.ORDINAL and int(row_value) > int(col_value):
                            self.current_grid.SetCellValue(i, j, "✘")
                        if int(row_value) == int(col_value):
                            self.current_grid.SetCellValue(i, j, "✘")
                self.datastorage.scaling_type = constants.INT

            if type == constants.INTERORDINAL:
                max_value = self.check_int_col(labelevent.GetCol())
                self.current_grid.DeleteCols(0, self.current_grid.GetNumberCols())
                self.current_grid.DeleteRows(0, self.current_grid.GetNumberRows())
                self.current_grid.AppendCols(2*(max_value+1))
                self.current_grid.AppendRows(max_value+1)

                for a in range(2*(max_value+1)):
                    if a < max_value+1:
                        self.current_grid.SetColLabelValue(a, "≤" + str(a))
                    else:
                        self.current_grid.SetColLabelValue(a, "≥" + str(a - (max_value+1)))
                for i in range(self.current_grid.GetNumberRows()):
                    self.current_grid.SetRowLabelValue(i, str(i))
                    for j in range(i, i+(max_value+1)+1):
                        self.current_grid.SetCellValue(i, j, "✘")
                self.datastorage.scaling_type = constants.INT

            self.current_grid.EnableEditing(False)
            self.frame.csvtabs.SetSelection(len(self.datastorage.tabs) - 1)

        return to_scaling

    def new_tab(self, name):

        new_grid = grid.Grid(self.frame.csvtabs)
        new_grid.CreateGrid(16, 8)
        new_grid.EnableDragCell()
        new_grid.EnableDragColMove()
        new_grid.Bind(grid.EVT_GRID_CELL_CHANGED, self.datastorage.set_edited)
        new_grid.Bind(grid.EVT_GRID_LABEL_RIGHT_CLICK, self.mservice.label_menu)
        new_grid.Bind(grid.EVT_GRID_CELL_RIGHT_CLICK, self.mservice.cell_menu)
        new_grid.Bind(grid.EVT_GRID_CELL_LEFT_CLICK, self.check_toggle)
        self.frame.csvtabs.AddPage(new_grid, "Scaling:"+name)
        self.current_grid = new_grid
        self.datastorage.tabs.append(new_grid)

    def view_result(self, evt=None):
        self.get_save_to_storage(self.frame.csvtabs.GetSelection())
        self.current_grid.DeleteRows(0, self.current_grid.GetNumberRows())
        if not self.current_grid.GetCornerLabelValue() == "":
            scaling = self.datastorage.table.scalings[self.current_grid.GetCornerLabelValue()]
            scaling_col_labels = scaling[1]
            scaling_table = scaling[2]
            scaling_type = scaling[3]
        # Ascertain Scaled Attribute
        col_numer = 0
        for col in range(len(self.datastorage.table.col_labels)):
            if self.datastorage.table.col_labels[col] == self.current_grid.GetCornerLabelValue():
                col_numer = col
                break
        for i in range(len(self.datastorage.table.row_labels)):
            self.current_grid.AppendRows(1)
            self.current_grid.SetRowLabelValue(i, self.datastorage.table.row_labels[i])
            if scaling_type == constants.INT:
                if self.datastorage.table.original[(i, col_numer)] != "":
                    value = int(self.datastorage.table.original[(i, col_numer)])
                    for j in range(len(scaling_col_labels)):
                        self.current_grid.SetCellValue(i, j, scaling_table[value, j])
            if scaling_type == constants.GENERIC:
                if self.datastorage.table.original[(i, col_numer)] != "":
                    value = self.datastorage.table.original[(i, col_numer)]
                    for j in range(len(scaling_col_labels)):
                        self.current_grid.SetCellValue(i, j, scaling_table[scaling_col_labels.index(value), j])

        self.datastorage.table_state = constants.RESULT
        self.frame.csvtabs.SetPageText(self.frame.csvtabs.GetSelection(), "Result:"+self.current_grid.GetCornerLabelValue())

    def get_save_to_storage(self, evt=None):
        def save_to_storage(evt=None):

            # Save Original Table
            if self.frame.csvtabs.GetSelection() == 0:
                if self.datastorage.expanded:
                    return
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
            if self.frame.csvtabs.GetSelection() > 0:

                row_labels = list()
                col_labels = list()
                scaling_grid = self.datastorage.tabs[self.frame.csvtabs.GetSelection()]
                for a in range(scaling_grid.GetNumberRows()):
                    row_labels.append(scaling_grid.GetRowLabelValue(a))
                for b in range(scaling_grid.GetNumberCols()):
                    col_labels.append(scaling_grid.GetColLabelValue(b))

                table = dict()
                for i in range(scaling_grid.GetNumberRows()):
                    for j in range(scaling_grid.GetNumberCols()):
                        table[(i, j)] = scaling_grid.GetCellValue(i, j)

                self.datastorage.table.set_scaling(scaling_grid.GetCornerLabelValue(), row_labels, col_labels, table, self.datastorage.scaling_type)
            self.current_grid = self.datastorage.tabs[self.frame.csvtabs.GetSelection()]
            print(self.datastorage.table.col_labels)
        return save_to_storage

    def load_from_storage(self, target):

        self.current_grid.DeleteRows(0, self.current_grid.GetNumberRows())
        self.current_grid.DeleteCols(0, self.current_grid.GetNumberCols())

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

        self.current_grid.AppendCols(len(col_labels))
        for a in range(len(col_labels)):
            self.current_grid.SetColLabelValue(a, col_labels[a])
        self.current_grid.AppendRows(len(row_labels))
        for a in range(len(row_labels)):
            self.current_grid.SetRowLabelValue(a, row_labels[a])
        for coords, value in table.items():
            self.current_grid.SetCellValue(coords[0], coords[1], value)
        self.current_grid.SetCornerLabelValue(target)
        self.datastorage.table_state = constants.SCALING
        self.frame.csvtabs.SetPageText(self.frame.csvtabs.GetSelection(), "Scaling:"+target)

    def check_int_col(self, col):

        maxvalue = 0
        for i in range(self.frame.grid.GetNumberRows()):
            value = self.frame.grid.GetCellValue(i, col)
            if not (value.isnumeric() or value == ""):
                return None
            if value.isnumeric():
                maxvalue = max(maxvalue, int(value))
        return maxvalue

    def check_toggle(self, evt):
        if self.frame.csvtabs.GetSelection() > 0 and self.datastorage.table_state != constants.RESULT:
            if self.current_grid.GetCellValue(evt.GetRow(), evt.GetCol()) == "":
                self.current_grid.SetCellValue(evt.GetRow(), evt.GetCol(), "✘")
            else:
                self.current_grid.SetCellValue(evt.GetRow(), evt.GetCol(), "")
        else:
            evt.Skip()

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

            if self.col_name_taken(name):
                errortext = 'Attribute Names Must be Unique.'
                dialog = wx.MessageDialog(None, errortext, '', wx.ICON_WARNING | wx.OK)
                dialog.ShowModal()
                return
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

            if self.col_name_taken(name):
                errortext = 'Attribute Names Must be Unique.'
                dialog = wx.MessageDialog(None, errortext, '', wx.ICON_WARNING | wx.OK)
                dialog.ShowModal()
                return
            if name != "":
                self.frame.grid.AppendCols()
                self.frame.grid.SetColLabelValue(self.frame.grid.GetNumberCols()-1, name)
                self.cascade_col(labelevent.GetCol())
                self.datastorage.set_edited()

        return add_col

    def col_name_taken(self, string):
        for i in range(self.frame.grid.GetNumberCols()):
            if self.frame.grid.GetColLabelValue(i) == string:
                return True
        return False

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

