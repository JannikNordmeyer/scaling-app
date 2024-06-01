from wx import grid
import wx


def delete_cols(grid):
    # Deletes all Columns from the Specified Grid.
    # Needed to Circumvent Bug with Deletion after the Column Order has been Changed.
    while grid.GetNumberCols() > 0:
        grid.DeleteCols(0, grid.GetNumberCols())


def get_grid_data(grid):
    # Reads Data Necessary for API Requests from Input Grid

    objects = []
    for i in range(grid.GetNumberRows()):
        objects.append(grid.GetRowLabelValue(i))

    attributes = []
    for j in range(grid.GetNumberCols()):
        attributes.append(grid.GetColLabelValue(j))

    incidence = []
    for i in range(grid.GetNumberRows()):
        for j in range(grid.GetNumberCols()):
            if grid.GetCellValue(i, j) != "":
                incidence.append([grid.GetRowLabelValue(i), grid.GetColLabelValue(j)])

    return objects, attributes, incidence


class TableSubService:

    def __init__(self, tservice, frame, datastorage):
        self.frame = frame
        self.datastorage = datastorage

        # Superservient Tableservice
        self.s = tservice

    def dye_col(self, col, color):
        # Sets background color of all cells in specified column
        for i in range(self.frame.many_valued_grid.GetNumberRows()):
            self.frame.many_valued_grid.SetCellBackgroundColour(i, col, color)
        self.frame.many_valued_grid.ForceRefresh()

    def new_tab(self, name):
        # Creates new Grid Tab for Scaling
        new_grid = grid.Grid(self.frame.scaling_tabs)
        new_grid.CreateGrid(1, 1)
        new_grid.EnableDragCell()
        new_grid.EnableDragColMove()
        new_grid.Bind(grid.EVT_GRID_CELL_CHANGED, self.datastorage.set_edited)
        new_grid.Bind(grid.EVT_GRID_LABEL_RIGHT_CLICK, self.s.mservice.scaling_label_menu)
        new_grid.Bind(grid.EVT_GRID_CELL_RIGHT_CLICK, self.s.mservice.scaling_cell_menu)
        new_grid.Bind(grid.EVT_GRID_CELL_LEFT_CLICK, self.s.check_toggle)
        self.frame.scaling_tabs.AddPage(new_grid, "Scale:" + name)
        self.s.current_grid = new_grid
        self.datastorage.grid_tabs.append(new_grid)

    def check_numeric_col(self, col):
        # Return the Minimum and Maximum Values, if all Entries are Numbers, otherwise False.

        maxvalue = 0
        minvalue = 0
        for i in range(self.frame.many_valued_grid.GetNumberRows()):
            value = self.frame.many_valued_grid.GetCellValue(i, col)

            try:
                maxvalue = max(maxvalue, float(value))
                minvalue = min(minvalue, float(value))
            except:
                if value != "":
                    return False

        return minvalue, maxvalue

    def get_col_entries(self, col, attribute):
        # Returns all unique values from specified attribute in main grid
        # and sorts them based on order specified in statistics tab
        entries = set()
        for i in range(self.frame.many_valued_grid.GetNumberRows()):
            value = self.frame.many_valued_grid.GetCellValue(i, col)
            if value != "":
                entries.add(value)
        entries = list(entries)

        affected_tab = None
        for stats_tab in self.datastorage.stats:
            if stats_tab.attribute == attribute:
                affected_tab = stats_tab
        if affected_tab is not None and affected_tab.order_dict is not None:
            entries.sort(key=lambda val: affected_tab.order_dict[val])
        elif self.check_numeric_col(col):
            entries.sort(key=float)
        else:
            entries.sort()

        return entries

    def get_delete_row(self, row):
        def delete_row(evt=None):
            # deletes specified row
            for i in range(self.s.current_grid.GetNumberRows() - row):
                self.s.current_grid.SetRowLabelValue(row + i, self.s.current_grid.GetRowLabelValue(row + i + 1))
            self.s.current_grid.DeleteRows(pos=row)
            self.datastorage.edited = True
            self.s.table_edited()

        return delete_row

    def get_purge_row(self, labelevent):
        def purge_row(evt):
            # clears all values in the specified row
            if not self.is_empty():
                self.datastorage.edited = True
            for i in range(self.s.current_grid.GetNumberCols()):
                self.s.current_grid.SetCellValue(labelevent.GetRow(), i, "")
            self.s.table_edited()

        return purge_row

    def get_flood_row(self, labelevent):
        def flood_row(evt):
            # fills in all cells in the row
            if not self.is_empty():
                self.datastorage.edited = True
            for i in range(self.s.current_grid.GetNumberCols()):
                self.s.current_grid.SetCellValue(labelevent.GetRow(), i, "✘")
            self.s.table_edited()

        return flood_row

    def get_edit_row_label(self, labelevent):
        def edit_row_label(evt):
            dialog = wx.TextEntryDialog(None, "Row name:", caption="New Row", value="",
                                        style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
            dialog.ShowModal()
            name = dialog.GetValue()
            dialog.Destroy()
            if name != "":
                self.s.current_grid.SetRowLabelValue(labelevent.GetRow(), name)
                self.datastorage.set_edited()
            self.s.table_edited()

        return edit_row_label

    def get_add_row(self, labelevent):
        def add_row(evt):
            dialog = wx.TextEntryDialog(None, "Row name:", caption="New Row", value="",
                                        style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
            dialog.ShowModal()
            name = dialog.GetValue()
            dialog.Destroy()
            if name != "":
                self.s.current_grid.AppendRows()
                self.cascade_row(labelevent.GetRow())
                self.s.current_grid.SetRowLabelValue(labelevent.GetRow() + 1, name)
                self.datastorage.set_edited()
                self.s.table_edited()

        return add_row

    def get_delete_col(self, col):
        def delete_col(evt=None):
            if self.frame.scaling_tabs.GetSelection() == 0:
                attribute = self.frame.many_valued_grid.GetColLabelValue(col)
                self.s.get_delete_selected_scaling(attribute)()

            self.s.current_grid.DeleteCols(pos=self.s.current_grid.GetColPos(col), updateLabels=False)
            self.datastorage.set_edited()
            self.s.table_edited()

        return delete_col

    def get_purge_col(self, labelevent):
        def purge_col(evt):
            if not self.is_empty():
                self.datastorage.set_edited()
            for i in range(self.s.current_grid.GetNumberRows()):
                self.s.current_grid.SetCellValue(i, labelevent.GetCol(), "")
            self.s.table_edited()

        return purge_col

    def get_flood_col(self, labelevent):
        def flood_col(evt):
            if not self.is_empty():
                self.datastorage.set_edited()
            for i in range(self.s.current_grid.GetNumberRows()):
                self.s.current_grid.SetCellValue(i, labelevent.GetCol(), "✘")
            self.s.table_edited()

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

                old_name = self.s.current_grid.GetColLabelValue(labelevent.GetCol())

                self.s.current_grid.SetColLabelValue(labelevent.GetCol(), name)
                self.datastorage.set_edited()

                # Replace All Occurrences of the Original Name with the New One
                if self.frame.scaling_tabs.GetSelection() == 0:
                    level = self.datastorage.table.attribute_levels.pop(old_name)
                    self.datastorage.table.attribute_levels[name] = level

                    if old_name in self.datastorage.table.scalings:
                        scaling = self.datastorage.table.scalings[old_name]
                        self.datastorage.table.scalings[name] = scaling

                        for i in range(self.frame.scaling_tabs.GetPageCount()):

                            if self.frame.scaling_tabs.GetPageText(i) == "Scale:" + old_name:
                                self.frame.scaling_tabs.SetPageText(i, "Scale:" + name)
                                self.datastorage.grid_tabs[i].SetCornerLabelValue(name)
                                break
                            if self.frame.scaling_tabs.GetPageText(i) == "Result:" + old_name:
                                self.frame.scaling_tabs.SetPageText(i, "Result:" + name)
                                self.datastorage.grid_tabs[i].SetCornerLabelValue(name)
                                break

                    if old_name in self.datastorage.stats_visible:
                        for i in range(self.frame.grid_tabs.GetPageCount()):
                            if self.frame.grid_tabs.GetPageText(i) == "Stats: " + old_name:
                                self.frame.grid_tabs.SetPageText(i, "Stats: " + name)
                                numberspecialtabs = 3
                                self.datastorage.stats[i - numberspecialtabs].attribute = name
                                break

            self.frame.scaling_tabs.Layout()
            self.frame.scaling_tabs.Update()
            self.s.table_edited()

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
                self.s.current_grid.AppendCols()
                self.s.current_grid.SetColLabelValue(self.s.current_grid.GetNumberCols() - 1, name)
                self.cascade_col(labelevent.GetCol())
                self.datastorage.set_edited()
            self.s.table_edited()

        return add_col

    def col_name_taken(self, string):
        for i in range(self.frame.many_valued_grid.GetNumberCols()):
            if self.s.current_grid.GetColLabelValue(i) == string:
                return True
        return False

    def cascade_row(self, pos):
        # Moves Final Row of the Table up to the Specified Position
        number_rows = self.s.current_grid.GetNumberRows()
        i = 0
        while i < number_rows - pos - 2:
            self.swap_row(number_rows - 2 - i, number_rows - 1 - i)
            i += 1

    def swap_row(self, a, b):

        temp = self.s.current_grid.GetRowLabelValue(a)
        self.s.current_grid.SetRowLabelValue(a, self.s.current_grid.GetRowLabelValue(b))
        self.s.current_grid.SetRowLabelValue(b, temp)
        for i in range(self.s.current_grid.GetNumberCols()):

            temp = self.s.current_grid.GetCellValue(a, i)
            self.s.current_grid.SetCellValue(a, i, self.s.current_grid.GetCellValue(b, i))
            self.s.current_grid.SetCellValue(b, i, temp)

    def cascade_col(self, pos):
        number_cols = self.s.current_grid.GetNumberCols()
        i = 0
        while i < number_cols - pos - 2:
            self.swap_col(number_cols - 2 - i, number_cols - 1 - i)
            i += 1

    def swap_col(self, a, b):
        # Moves Final Column of the Table up to the Specified Position
        temp = self.s.current_grid.GetColLabelValue(a)
        self.s.current_grid.SetColLabelValue(a, self.s.current_grid.GetColLabelValue(b))
        self.s.current_grid.SetColLabelValue(b, temp)
        for i in range(self.s.current_grid.GetNumberRows()):

            temp = self.s.current_grid.GetCellValue(i, a)
            self.s.current_grid.SetCellValue(i, a, self.s.current_grid.GetCellValue(i, b))
            self.s.current_grid.SetCellValue(i, b, temp)

    def purge_table(self, evt=None):
        if not self.is_empty():
            self.datastorage.set_edited()
            self.s.current_grid.ClearGrid()
            self.s.table_edited()
            self.s.sservice.clear_stats()

    def reset_table(self, evt=None):
        # Deletes All Data Relating to the Loaded Table and Resets it to it's Default State
        self.frame.many_valued_grid.DeleteRows(0, self.frame.many_valued_grid.GetNumberRows())
        delete_cols(self.frame.many_valued_grid)
        self.frame.many_valued_grid.AppendRows(16)
        self.frame.many_valued_grid.AppendCols(8)
        for i in range(self.frame.many_valued_grid.GetNumberRows()):
            self.frame.many_valued_grid.SetRowLabelValue(i, str(i + 1))
        self.s.sservice.clear_stats()
        self.s.clear_scalings()

    def is_empty(self):
        # Checks if Main Grid is Fully Empty
        for i in range(self.frame.many_valued_grid.GetNumberRows()):
            for j in range(self.frame.many_valued_grid.GetNumberCols()):
                if self.frame.many_valued_grid.GetCellValue(i, j) != "":
                    return False
        return True

    def col_empty(self, col):
        for i in range(self.frame.many_valued_grid.GetNumberRows()):
            if self.frame.many_valued_grid.GetCellValue(i, col) != "":
                return False
        return True

    def row_empty(self, row):
        for i in range(self.frame.many_valued_grid.GetNumberCols()):
            if self.frame.many_valued_grid.GetCellValue(row, i) != "":
                return False
        return True

    def value_in_data(self, value, col):
        # Checks if Specified Value is Part of the Data in the Specified Column in th Main Grid

        # Always Returns False if Main Grid is Currently Selected !!!
        if self.frame.scaling_tabs.GetSelection() == 0:
            return False
        if value == "":
            return False

        for i in range(self.frame.many_valued_grid.GetNumberRows()):
            if self.frame.many_valued_grid.GetCellValue(i, col) == value:
                return True
        return False

    def value_in_scaling(self, value, scaling):
        # Checks if Specified Value is Already in the Specified Scaling

        if scaling in self.datastorage.table.scalings:
            scaling_rows = self.datastorage.table.scalings[scaling][0]
            return value in scaling_rows
        else:
            # If Scaling Doesn't Exist, Cell May be Edited as Normal
            return True

    def current_attribute(self):
        # Returns the Attribute Represented by the Currently Selected Scaling Table
        return self.frame.scaling_tabs.GetPage(self.frame.scaling_tabs.GetSelection()).GetCornerLabelValue()

    def drop_empty_cols(self, evt=None):
        i = 0
        while i < self.frame.many_valued_grid.GetNumberCols():
            if self.col_empty(i):
                self.s.get_delete_col(i)()
                i -= 1
            i += 1

    def drop_empty_rows(self, evt=None):
        i = 0
        while i < self.frame.many_valued_grid.GetNumberRows():
            if self.row_empty(i):
                self.s.get_delete_row(i)()
                i -= 1
            i += 1
