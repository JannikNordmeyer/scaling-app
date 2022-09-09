import csv
import wx
import wx.grid as grid
from scaling_app import constants, statistics


class TableService:

    def __init__(self, frame, datastorage):
        self.frame = frame
        self.datastorage = datastorage
        self.mservice = None
        self.sservice = None

        self.current_grid = None

    def fill_table(self):

        self.current_grid = self.frame.main_grid

        values = csv.reader(self.datastorage.data, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)

        self.frame.main_grid.DeleteRows(0, self.frame.main_grid.GetNumberRows())
        self.frame.main_grid.DeleteCols(0, self.frame.main_grid.GetNumberCols())
        self.frame.main_grid.AppendRows(values.line_num)

        rowlabellength = 0
        for row in values:

            if values.line_num == 1:
                rowlabellength = len(row)
                self.frame.main_grid.AppendCols(len(row))
                i = 0
                for entry in row:
                    self.frame.main_grid.SetColLabelValue(i, entry)
                    i += 1
            else:
                self.frame.main_grid.AppendRows(1)
                self.frame.main_grid.SetRowLabelValue(values.line_num - 2, str(values.line_num - 1))
                j = 0
                first = True
                for entry in row:
                    if len(row) == rowlabellength + 1 and first:
                        self.frame.main_grid.SetRowLabelValue(values.line_num - 2, entry)
                        first = False
                        continue
                    self.frame.main_grid.SetCellValue(values.line_num - 2, j, entry)
                    j += 1
        self.frame.main_grid.SetRowLabelSize(grid.GRID_AUTOSIZE)
        self.frame.main_grid.SetCornerLabelValue("")

    def load_expanded(self, evt=None):

        if self.frame.result_grid.GetNumberCols() > 0:
            self.frame.result_grid.DeleteCols(0, self.frame.result_grid.GetNumberCols())

        # Reload Rows in case the Dataset Changed
        if self.frame.result_grid.GetNumberRows() > 0:
            self.frame.result_grid.DeleteRows(0, self.frame.result_grid.GetNumberRows())
            for i in range(self.frame.main_grid.GetNumberRows()):
                self.frame.result_grid.AppendRows(1)
                self.frame.result_grid.SetRowLabelValue(i, self.frame.main_grid.GetRowLabelValue(i))

        for i in range(len(self.datastorage.table.col_labels), -1, -1):
            self.get_expand_column(i)()

    def get_expand_column(self, col):
        def expand_column(evt=None):

            if self.frame.main_grid.GetColLabelValue(col) not in self.datastorage.table.scalings:
                return
            scaling = self.datastorage.table.scalings[self.frame.main_grid.GetColLabelValue(col)]
            row_labels = scaling[0]
            col_labels = scaling[1]
            scaling_table = scaling[2]

            col_offset = self.frame.result_grid.GetNumberCols()
            self.frame.result_grid.AppendCols(len(col_labels))
            for new_col in range(len(col_labels)):
                self.frame.result_grid.SetColLabelValue(col_offset + new_col, self.frame.main_grid.GetColLabelValue(col) + ":\n" + col_labels[new_col])

            for i in range(self.frame.main_grid.GetNumberRows()):
                if self.frame.main_grid.GetCellValue(i, col) != "":
                    value = self.frame.main_grid.GetCellValue(i, col)
                    for j in range(len(col_labels)):
                        self.frame.result_grid.SetCellValue(i, col_offset + j, scaling_table[(row_labels.index(value), j)])

        return expand_column

    def get_to_scaling(self, labelevent, type):
        def to_scaling(evt=None):

            # load from storage if scaling exists and right tab is selected
            if self.current_grid.GetCornerLabelValue() in self.datastorage.table.scalings:
                self.load_from_storage(self.current_grid.GetCornerLabelValue())
                self.datastorage.result_visible.discard(self.current_grid.GetCornerLabelValue())
                return

            # Add new tab if scaling doesn't exist
            self.get_save_to_storage(self.frame.csvtabs.GetSelection())()

            self.new_tab(self.frame.main_grid.GetColLabelValue(labelevent.GetCol()))
            self.current_grid.SetCornerLabelValue(self.frame.main_grid.GetColLabelValue(labelevent.GetCol()))

            if type == constants.EMPTY or type == constants.DIAGONAL_ANY:
                values = list()
                for i in range(self.frame.main_grid.GetNumberRows()):
                    if self.frame.main_grid.GetCellValue(i, labelevent.GetCol()) not in values:
                        if self.frame.main_grid.GetCellValue(i, labelevent.GetCol()) != "":
                            values.append(self.frame.main_grid.GetCellValue(i, labelevent.GetCol()))
                self.current_grid.DeleteCols(0, self.current_grid.GetNumberCols())
                self.current_grid.DeleteRows(0, self.current_grid.GetNumberRows())
                self.current_grid.AppendCols(len(values))
                self.current_grid.AppendRows(len(values))
                for i in range(self.current_grid.GetNumberRows()):
                    self.current_grid.SetColLabelValue(i, values[i])
                    self.current_grid.SetRowLabelValue(i, values[i])
                    if type == constants.DIAGONAL_ANY:
                        self.current_grid.SetCellValue(i, i, "✘")

            if type == constants.DIAGONAL or type == constants.ORDINAL:
                limits = self.check_int_col(labelevent.GetCol())
                columns = list(range(limits[0], limits[1]+1))
                data_values = list()
                for i in range(self.frame.main_grid.GetNumberRows()):
                    value = self.frame.main_grid.GetCellValue(i, labelevent.GetCol())
                    if value != "":
                        data_values.append(int(value))
                columns_actual = [x for x in columns if x in data_values]

                self.current_grid.DeleteCols(0, self.current_grid.GetNumberCols())
                self.current_grid.AppendCols(len(columns_actual))
                self.current_grid.DeleteRows(0, self.frame.main_grid.GetNumberRows())
                self.current_grid.AppendRows(len(columns_actual))
                for a in range(len(columns_actual)):
                    self.current_grid.SetColLabelValue(a, str(columns_actual[a]))
                    self.current_grid.SetRowLabelValue(a, str(columns_actual[a]))
                for i in range(self.current_grid.GetNumberRows()):
                    row_value = self.current_grid.GetRowLabelValue(i)
                    for j in range(self.current_grid.GetNumberCols()):
                        col_value = self.current_grid.GetColLabelValue(j)
                        if type == constants.ORDINAL and int(row_value) > int(col_value):
                            self.current_grid.SetCellValue(i, j, "✘")
                        if int(row_value) == int(col_value):
                            self.current_grid.SetCellValue(i, j, "✘")

            if type == constants.INTERORDINAL:
                limits = self.check_int_col(labelevent.GetCol())
                columns = list(range(limits[0], limits[1] + 1))
                data_values = list()

                for i in range(self.frame.main_grid.GetNumberRows()):
                    value = self.frame.main_grid.GetCellValue(i, labelevent.GetCol())
                    if value != "":
                        data_values.append(int(value))

                columns_actual = [x for x in columns if x in data_values]

                self.current_grid.DeleteCols(0, self.current_grid.GetNumberCols())
                self.current_grid.AppendCols(2*len(columns_actual))
                self.current_grid.DeleteRows(0, self.frame.main_grid.GetNumberRows())
                self.current_grid.AppendRows(len(columns_actual))

                for a in range(2*(len(columns_actual))):
                    if a < limits[1]:
                        self.current_grid.SetColLabelValue(a, "≤" + str(columns_actual[a]))
                    else:
                        self.current_grid.SetColLabelValue(a, "≥" + str(columns_actual[a - (limits[1])]))
                for i in range(self.current_grid.GetNumberRows()):
                    self.current_grid.SetRowLabelValue(i, str(columns_actual[i]))
                    for j in range(i, i+(limits[1]+1)):
                        self.current_grid.SetCellValue(i, j, "✘")

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
        self.get_save_to_storage(self.frame.csvtabs.GetSelection())()
        self.current_grid = self.datastorage.tabs[self.frame.csvtabs.GetSelection()]
        self.current_grid.DeleteRows(0, self.current_grid.GetNumberRows())

        scaling = self.datastorage.table.scalings[self.current_grid.GetCornerLabelValue()]
        scaling_row_labels = scaling[0]
        scaling_col_labels = scaling[1]
        scaling_table = scaling[2]
        # Ascertain Column of Scaled Attribute in Main Grid
        col_number = 0
        for col in range(len(self.datastorage.table.col_labels)):
            if self.datastorage.table.col_labels[col] == self.current_grid.GetCornerLabelValue():
                col_number = col
                break

        for i in range(len(self.datastorage.table.row_labels)):
            self.current_grid.AppendRows(1)
            self.current_grid.SetRowLabelValue(i, self.datastorage.table.row_labels[i])

            if self.datastorage.table.original[(i, col_number)] != "":
                value = self.datastorage.table.original[(i, col_number)]
                for j in range(len(scaling_col_labels)):
                    self.current_grid.SetCellValue(i, j, scaling_table[scaling_row_labels.index(value), j])

        self.datastorage.result_visible.add(self.current_grid.GetCornerLabelValue())
        self.frame.csvtabs.SetPageText(self.frame.csvtabs.GetSelection(), "Result:"+self.current_grid.GetCornerLabelValue())

    def get_save_to_storage(self, evt=None):
        def save_to_storage(evt=None):
            # -----Called When Tab Changes-----

            self.current_grid = self.datastorage.tabs[self.frame.csvtabs.GetSelection()]

            # Save Original Table
            self.datastorage.table.col_labels.clear()
            self.datastorage.table.row_labels.clear()
            self.datastorage.table.original.clear()

            for a in range(self.frame.main_grid.GetNumberCols()):
                self.datastorage.table.col_labels.append(self.frame.main_grid.GetColLabelValue(a))
            for b in range(self.frame.main_grid.GetNumberRows()):
                self.datastorage.table.row_labels.append(self.frame.main_grid.GetRowLabelValue(b))

            for i in range(self.frame.main_grid.GetNumberRows()):
                for j in range(self.frame.main_grid.GetNumberCols()):
                    self.datastorage.table.original[(i, j)] = self.frame.main_grid.GetCellValue(i, j)

            # Save Current Scaling
            if self.frame.csvtabs.GetSelection() >= 2 and self.current_grid.GetCornerLabelValue() not in self.datastorage.result_visible:

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

                self.datastorage.table.set_scaling(scaling_grid.GetCornerLabelValue(), row_labels, col_labels, table)
            self.current_grid = self.datastorage.tabs[self.frame.csvtabs.GetSelection()]
            self.load_expanded()
        return save_to_storage

    def table_edited(self):
        # Save current tables, then reset scalings to account for table changes
        for i in range(len(self.datastorage.tabs)):
            self.get_save_to_storage(i)()
            if i >= 2:
                self.current_grid = self.datastorage.tabs[i]
                self.get_to_scaling(labelevent=None, type=None)()
        self.current_grid = self.datastorage.tabs[self.frame.csvtabs.GetSelection()]
        self.load_expanded()
        self.sservice.update_stats()

    def load_from_storage(self, target):

        self.current_grid.DeleteRows(0, self.current_grid.GetNumberRows())
        self.current_grid.DeleteCols(0, self.current_grid.GetNumberCols())

        # Load Original
        if target == constants.ORIGINAL:

            self.frame.main_grid.AppendCols(len(self.datastorage.table.col_labels))
            for a in range(len(self.datastorage.table.col_labels)):
                self.frame.main_grid.SetColLabelValue(a, self.datastorage.table.col_labels[a])
            self.frame.main_grid.AppendRows(len(self.datastorage.table.row_labels))
            for b in range(len(self.datastorage.table.row_labels)):
                self.frame.main_grid.SetRowLabelValue(b, self.datastorage.table.row_labels[b])
            for coords, value in self.datastorage.table.original.items():
                self.frame.main_grid.SetCellValue(coords[0], coords[1], value)
            self.current_grid = self.datastorage.tabs[self.frame.csvtabs.GetSelection()]
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
        self.frame.csvtabs.SetPageText(self.datastorage.tabs.index(self.current_grid), "Scaling:" + target)
        self.current_grid = self.datastorage.tabs[self.frame.csvtabs.GetSelection()]

    def check_int_col(self, col):

        maxvalue = 0
        minvalue = 0
        for i in range(self.frame.main_grid.GetNumberRows()):
            value = self.frame.main_grid.GetCellValue(i, col)
            if not (value.isnumeric() or value == ""):
                return False
            if value.isnumeric():
                maxvalue = max(maxvalue, int(value))
                minvalue = min(minvalue, int(value))
        return (minvalue, maxvalue)

    def check_toggle(self, evt):
        if self.frame.csvtabs.GetSelection() >= 2 and "Result:" not in self.frame.csvtabs.GetPageText(self.frame.csvtabs.GetSelection()):
            self.current_grid = self.datastorage.tabs[self.frame.csvtabs.GetSelection()]
            if self.current_grid.GetCellValue(evt.GetRow(), evt.GetCol()) == "":
                self.current_grid.SetCellValue(evt.GetRow(), evt.GetCol(), "✘")
            else:
                self.current_grid.SetCellValue(evt.GetRow(), evt.GetCol(), "")
            self.get_save_to_storage()()
            self.load_expanded()
        else:
            evt.Skip()

    def get_delete_row(self, labelevent):
        def delete_row(evt):
            for i in range(self.current_grid.GetNumberRows() - labelevent.GetRow()):
                self.current_grid.SetRowLabelValue(labelevent.GetRow() + i, self.current_grid.GetRowLabelValue(labelevent.GetRow() + i + 1))
            self.current_grid.DeleteRows(pos=labelevent.GetRow())
            self.datastorage.edited = True
            self.table_edited()

        return delete_row

    def get_purge_row(self, labelevent):
        def purge_row(evt):
            if not self.is_empty():
                self.datastorage.edited = True
            for i in range(self.current_grid.GetNumberCols()):
                self.current_grid.SetCellValue(labelevent.GetRow(), i, "")
            self.table_edited()

        return purge_row

    def get_flood_row(self, labelevent):
        def flood_row(evt):
            if not self.is_empty():
                self.datastorage.edited = True
            for i in range(self.current_grid.GetNumberCols()):
                self.current_grid.SetCellValue(labelevent.GetRow(), i, "✘")
            self.table_edited()

        return flood_row

    def get_edit_row_label(self, labelevent):
        def edit_row_label(evt):
            dialog = wx.TextEntryDialog(None, "Row name:", caption="New Row", value="",
                                        style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
            dialog.ShowModal()
            name = dialog.GetValue()
            dialog.Destroy()
            if name != "":
                self.current_grid.SetRowLabelValue(labelevent.GetRow(), name)
                self.datastorage.set_edited()
            self.table_edited()

        return edit_row_label

    def get_add_row(self, labelevent):
        def add_row(evt):
            dialog = wx.TextEntryDialog(None, "Row name:", caption="New Row", value="",
                                        style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
            dialog.ShowModal()
            name = dialog.GetValue()
            dialog.Destroy()
            if name != "":
                self.current_grid.AppendRows()
                self.cascade_row(labelevent.GetRow())
                self.current_grid.SetRowLabelValue(labelevent.GetRow() + 1, name)
                self.datastorage.set_edited()
                self.table_edited()

        return add_row

    def get_delete_col(self, labelevent):
        def delete_col(evt):

            if self.frame.csvtabs.GetSelection() == 0:

                attribute = self.frame.main_grid.GetColLabelValue(labelevent.GetCol())
                self.get_delete_selected_scaling(attribute)()

            self.current_grid.DeleteCols(pos=labelevent.GetCol(), updateLabels=False)
            self.datastorage.set_edited()
            self.table_edited()

        return delete_col

    def get_delete_selected_scaling(self, attribute):
        def delete_selected_scaling(evt=None):

            if attribute in self.datastorage.table.scalings:
                for i in range(self.frame.csvtabs.GetPageCount()):
                    if self.frame.csvtabs.GetPageText(i) == "Scaling:" + attribute:
                        self.frame.csvtabs.DeletePage(i)
                        self.frame.csvtabs.SendSizeEvent()
                        self.datastorage.tabs.pop(i)
                self.datastorage.table.scalings.pop(attribute)
                self.frame.csvtabs.SetSelection(0)

        return delete_selected_scaling

    def get_purge_col(self, labelevent):
        def purge_col(evt):
            if not self.is_empty():
                self.datastorage.set_edited()
            for i in range(self.current_grid.GetNumberRows()):
                self.current_grid.SetCellValue(i, labelevent.GetCol(), "")
            self.table_edited()

        return purge_col

    def get_flood_col(self, labelevent):
        def flood_col(evt):
            if not self.is_empty():
                self.datastorage.set_edited()
            for i in range(self.current_grid.GetNumberRows()):
                self.current_grid.SetCellValue(i, labelevent.GetCol(), "✘")
            self.table_edited()

        return flood_col

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
                self.current_grid.SetColLabelValue(labelevent.GetCol(), name)
                self.datastorage.set_edited()
            self.table_edited()

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
                self.current_grid.AppendCols()
                self.current_grid.SetColLabelValue(self.current_grid.GetNumberCols() - 1, name)
                self.cascade_col(labelevent.GetCol())
                self.datastorage.set_edited()
            self.table_edited()

        return add_col

    def col_name_taken(self, string):
        for i in range(self.frame.main_grid.GetNumberCols()):
            if self.current_grid.GetColLabelValue(i) == string:
                return True
        return False

    def cascade_row(self, pos):
        number_rows = self.current_grid.GetNumberRows()
        i = 0
        while i < number_rows - pos - 2:
            self.swap_row(number_rows - 2 - i, number_rows - 1 - i)
            i += 1

    def swap_row(self, a, b):

        temp = self.current_grid.GetRowLabelValue(a)
        self.current_grid.SetRowLabelValue(a, self.current_grid.GetRowLabelValue(b))
        self.current_grid.SetRowLabelValue(b, temp)
        for i in range(self.current_grid.GetNumberCols()):

            temp = self.current_grid.GetCellValue(a, i)
            self.current_grid.SetCellValue(a, i, self.current_grid.GetCellValue(b, i))
            self.current_grid.SetCellValue(b, i, temp)

    def cascade_col(self, pos):
        number_cols = self.current_grid.GetNumberCols()
        i = 0
        while i < number_cols - pos - 2:
            self.swap_col(number_cols - 2 - i, number_cols - 1 - i)
            i += 1

    def swap_col(self, a, b):

        temp = self.current_grid.GetColLabelValue(a)
        self.current_grid.SetColLabelValue(a, self.current_grid.GetColLabelValue(b))
        self.current_grid.SetColLabelValue(b, temp)
        for i in range(self.current_grid.GetNumberRows()):

            temp = self.current_grid.GetCellValue(i, a)
            self.current_grid.SetCellValue(i, a, self.current_grid.GetCellValue(i, b))
            self.current_grid.SetCellValue(i, b, temp)

    def purge_table(self, evt):
        if not self.is_empty():
            self.datastorage.set_edited()
            self.current_grid.ClearGrid()
            self.table_edited()
            self.sservice.clear_stats()

    def reset_table(self, evt=None):

        self.frame.main_grid.DeleteRows(0, self.frame.main_grid.GetNumberRows())
        self.frame.main_grid.DeleteCols(0, self.frame.main_grid.GetNumberCols())
        self.frame.main_grid.AppendRows(16)
        self.frame.main_grid.AppendCols(8)
        for i in range(self.frame.main_grid.GetNumberRows()):
            self.frame.main_grid.SetRowLabelValue(i, str(i + 1))
        self.sservice.clear_stats()
        self.clear_scalings()

    def clear_scalings(self):
        self.datastorage.result_visible.clear()
        while len(self.datastorage.tabs) > 2:
            self.datastorage.tabs.pop()

        while self.frame.csvtabs.GetPageCount() > 2:
            self.frame.csvtabs.DeletePage(2)

    def is_empty(self):
        for i in range(self.frame.main_grid.GetNumberRows()):
            for j in range(self.frame.main_grid.GetNumberCols()):
                if self.frame.main_grid.GetCellValue(i, j) != "":
                    return False
        return True

    def value_in_data(self, value, col):

        # Always Returns False if Main Grid is Selected
        if self.frame.csvtabs.GetSelection() == 0:
            return False
        if value == "":
            return False

        for i in range(self.frame.main_grid.GetNumberRows()):
            if self.frame.main_grid.GetCellValue(i, col) == value:
                return True
        return False

    def value_in_scaling(self, value, scaling):

        if scaling in self.datastorage.table.scalings:
            scaling_rows = self.datastorage.table.scalings[scaling][0]
            return value in scaling_rows
        else:
            # If Scaling Doesn't Exist, Cell May be Edited as Normal
            return True

    def cell_changed(self, evt):
        self.datastorage.set_edited()
        self.sservice.update_stats()
        if self.frame.csvtabs.GetSelection() == 0:
            value = self.frame.main_grid.GetCellValue(evt.GetRow(), evt.GetCol())
            scaling = self.frame.main_grid.GetColLabelValue(evt.GetCol())
            if not self.value_in_scaling(value, scaling):
                scaling_rows = self.datastorage.table.scalings[scaling][0]
                scaling_cols = self.datastorage.table.scalings[scaling][1]
                scaling_table = self.datastorage.table.scalings[scaling][2]
                scaling_rows.append(value)
                for i in range(len(scaling_cols)):
                    scaling_table[len(scaling_rows)-1, i] = ""
                self.datastorage.table.set_scaling(scaling, scaling_rows, scaling_cols, scaling_table)

                # Ascertain Table of Scaling. Current Grid Will be Reset by load_from_storage()
                for tab in self.datastorage.tabs:
                    if tab.GetCornerLabelValue() == scaling:
                        self.current_grid = tab
                self.load_from_storage(scaling)

                errortext = 'The Value has been Added to the Scaling.'
                dialog = wx.MessageDialog(None, errortext, 'Entered Value is not Part of the Attributes Scaling', wx.ICON_WARNING | wx.OK)
                dialog.ShowModal()
