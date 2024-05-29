import wx

from scaling_app import tablesubservice, api, menuservice


class SimpleContextService:

    def __init__(self, frame, datastorage):
        self.datastorage = datastorage
        self.menuservice = None
        self.graphservice = None
        self.frame = frame

    def fill_context(self, objects, attributes, incidence):
        # Inputs context into the many valued grid
        if self.frame.single_valued_grid.GetNumberRows() > 0:
            self.frame.single_valued_grid.DeleteRows(0, self.frame.single_valued_grid.GetNumberRows())
        tablesubservice.delete_cols(self.frame.single_valued_grid)

        self.frame.single_valued_grid.AppendCols(len(attributes))
        for a in range(len(attributes)):
            self.frame.single_valued_grid.SetColLabelValue(a, attributes[a])
        self.frame.single_valued_grid.AppendRows(len(objects))
        for b in range(len(objects)):
            self.frame.single_valued_grid.SetRowLabelValue(b, objects[b])
        for coords, value in incidence.items():
            self.frame.single_valued_grid.SetCellValue(coords[0], coords[1], value)


    def toggle_cell(self, evt):
        # Toggles Selection of Context Cells
        if self.frame.single_valued_grid.GetCellValue(evt.GetRow(), evt.GetCol()) == "":
            self.frame.single_valued_grid.SetCellValue(evt.GetRow(), evt.GetCol(), "✘")
        else:
            self.frame.single_valued_grid.SetCellValue(evt.GetRow(), evt.GetCol(), "")

    def get_delete_row(self, row):
        def delete_row(evt=None):
            # deletes specified row
            for i in range(self.frame.single_valued_grid.GetNumberRows() - row):
                self.frame.single_valued_grid.SetRowLabelValue(row + i, self.frame.single_valued_grid.GetRowLabelValue(row + i + 1))
            self.frame.single_valued_grid.DeleteRows(pos=row)

        return delete_row

    def get_delete_col(self, col):
        def delete_col(evt=None):
            # deletes specified col
            self.frame.single_valued_grid.DeleteCols(pos=self.frame.single_valued_grid.GetColPos(col), updateLabels=False)

        return delete_col

    def get_edit_row_label(self, labelevent):
        def edit_row_label(evt):
            dialog = wx.TextEntryDialog(None, "Row name:", caption="New Row", value="",
                                        style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
            dialog.ShowModal()
            name = dialog.GetValue()
            dialog.Destroy()
            if name != "":
                self.frame.single_valued_grid.SetRowLabelValue(labelevent.GetRow(), name)

        return edit_row_label

    def get_edit_col_label(self, labelevent):
        def edit_col_label(evt):
            dialog = wx.TextEntryDialog(None, "Column name:", caption="New Column", value="",
                                        style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
            dialog.ShowModal()
            name = dialog.GetValue()
            dialog.Destroy()
            if name != "":
                self.frame.single_valued_grid.SetColLabelValue(labelevent.GetCol(), name)

        return edit_col_label

    def get_add_row(self, labelevent):
        def add_row(evt):
            dialog = wx.TextEntryDialog(None, "Row name:", caption="New Row", value="",
                                        style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
            dialog.ShowModal()
            name = dialog.GetValue()
            dialog.Destroy()
            if name != "":
                self.frame.single_valued_grid.AppendRows()
                self.cascade_row(labelevent.GetRow())
                self.frame.single_valued_grid.SetRowLabelValue(labelevent.GetRow() + 1, name)


        return add_row

    def get_add_col(self, labelevent):
        def add_col(evt):
            dialog = wx.TextEntryDialog(None, "Column name:", caption="New Column", value="",
                                        style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
            dialog.ShowModal()
            name = dialog.GetValue()
            dialog.Destroy()
            if name != "":
                self.frame.single_valued_grid.AppendCols()
                self.frame.single_valued_grid.SetColLabelValue(self.frame.single_valued_grid.GetNumberCols() - 1, name)
                self.cascade_col(labelevent.GetCol())

        return add_col

    def cascade_row(self, pos):
        # Moves Final Row of the Table up to the Specified Position
        number_rows = self.frame.single_valued_grid.GetNumberRows()
        i = 0
        while i < number_rows - pos - 2:
            self.swap_row(number_rows - 2 - i, number_rows - 1 - i)
            i += 1

    def cascade_col(self, pos):
        number_cols = self.frame.single_valued_grid.GetNumberCols()
        i = 0
        while i < number_cols - pos - 2:
            self.swap_col(number_cols - 2 - i, number_cols - 1 - i)
            i += 1

    def swap_row(self, a, b):

        temp = self.frame.single_valued_grid.GetRowLabelValue(a)
        self.frame.single_valued_grid.SetRowLabelValue(a, self.frame.single_valued_grid.GetRowLabelValue(b))
        self.frame.single_valued_grid.SetRowLabelValue(b, temp)
        for i in range(self.frame.single_valued_grid.GetNumberCols()):

            temp = self.frame.single_valued_grid.GetCellValue(a, i)
            self.frame.single_valued_grid.SetCellValue(a, i, self.frame.single_valued_grid.GetCellValue(b, i))
            self.frame.single_valued_grid.SetCellValue(b, i, temp)

    def swap_col(self, a, b):
        # Moves Final Column of the Table up to the Specified Position
        temp = self.frame.single_valued_grid.GetColLabelValue(a)
        self.frame.single_valued_grid.SetColLabelValue(a, self.frame.single_valued_grid.GetColLabelValue(b))
        self.frame.single_valued_grid.SetColLabelValue(b, temp)
        for i in range(self.frame.single_valued_grid.GetNumberRows()):

            temp = self.frame.single_valued_grid.GetCellValue(i, a)
            self.frame.single_valued_grid.SetCellValue(i, a, self.frame.single_valued_grid.GetCellValue(i, b))
            self.frame.single_valued_grid.SetCellValue(i, b, temp)


    def purge_table(self, evt=None):
        self.frame.single_valued_grid.ClearGrid()

    def reset_table(self, evt=None):
        self.frame.single_valued_grid.DeleteRows(0, self.frame.many_valued_grid.GetNumberRows())
        tablesubservice.delete_cols(self.frame.single_valued_grid)
        self.frame.single_valued_grid.AppendRows(16)
        self.frame.single_valued_grid.AppendCols(8)
        for i in range(self.frame.single_valued_grid.GetNumberRows()):
            self.frame.single_valued_grid.SetRowLabelValue(i, str(i + 1))

    def get_draw_lattice(self, draw_type, evt=None):
        def draw_lattice(evt=None):

            wx.BeginBusyCursor()
            objects, attributes, incidence = tablesubservice.get_grid_data(self.frame.single_valued_grid)

            try:

                lattice = api.request_lattice_layout(self.menuservice.api_address, objects, attributes, incidence, draw_type)
            except:
                menuservice.connection_error_dialog()
                wx.EndBusyCursor()
                return

            self.datastorage.lattice = lattice['layout']['result']
            self.graphservice.create_lattice_graph()
            wx.EndBusyCursor()

        return draw_lattice

