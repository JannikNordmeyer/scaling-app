import csv
import wx
import wx.grid as grid
from scaling_app import constants, menuservice
from scaling_app import api
from scaling_app.tablesubservice import TableSubService, delete_cols, get_grid_data


class TableService:

    def __init__(self, frame, datastorage):
        self.frame = frame
        self.datastorage = datastorage
        self.mservice = None
        self.sservice = None
        self.gservice = None

        self.current_grid = None

        # Subservice
        self.s = TableSubService(self, self.frame, self.datastorage)

    def fill_table(self):

        # Loads Table Contents from CSV in datastorage
        self.current_grid = self.frame.many_valued_grid

        values = csv.reader(self.datastorage.data, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)

        self.frame.many_valued_grid.DeleteRows(0, self.frame.many_valued_grid.GetNumberRows())
        delete_cols(self.frame.many_valued_grid)
        self.frame.many_valued_grid.AppendRows(values.line_num)

        rowlabellength = 0
        for row in values:

            if values.line_num == 1:
                # Read Column Names
                rowlabellength = len(row)
                self.frame.many_valued_grid.AppendCols(len(row))
                i = 0
                for entry in row:
                    self.frame.many_valued_grid.SetColLabelValue(i, entry)
                    i += 1
            else:
                self.frame.many_valued_grid.AppendRows(1)
                # Assign Number to Row Labels
                self.frame.many_valued_grid.SetRowLabelValue(values.line_num - 2, str(values.line_num - 1))
                j = 0
                first = True
                for entry in row:
                    if len(row) == rowlabellength + 1 and first:
                        # Replace Row Label, if File is Formatted Accordingly
                        self.frame.many_valued_grid.SetRowLabelValue(values.line_num - 2, entry)
                        first = False
                        continue
                    self.frame.many_valued_grid.SetCellValue(values.line_num - 2, j, entry)
                    j += 1
        self.frame.many_valued_grid.SetRowLabelSize(grid.GRID_AUTOSIZE)
        self.frame.many_valued_grid.SetCornerLabelValue("")
        self.check_attribute_levels()

    def check_attribute_levels(self):
        # Calculates Maximum Level of Measurements for Each Column
        for i in range(self.frame.many_valued_grid.GetNumberCols()):
            if self.s.check_numeric_col(i):
                self.datastorage.table.attribute_levels[self.frame.many_valued_grid.GetColLabelValue(i)] = constants.LEVEL_RAT
                self.s.dye_col(i, constants.LEVEL_RAT_COLOR)
            else:
                self.datastorage.table.attribute_levels[self.frame.many_valued_grid.GetColLabelValue(i)] = constants.LEVEL_NOM
                self.s.dye_col(i, constants.LEVEL_NOM_COLOR)

    def get_set_level(self, col, attribute, level):
        def set_level(evt=None):
            # Assigns level of measurement to specified attribute
            self.datastorage.table.attribute_levels[attribute] = level
            self.s.dye_col(col, constants.color_conv(level))

            # opens the stats screen, if the attribute is not numeric and the ordinal level of measurement is selected.
            if not self.s.check_numeric_col(col) and level == constants.LEVEL_ORD:
                self.sservice.get_add_stats(col=col, attribute=attribute)()
        return set_level

    def update_result_grid(self, evt=None):
        if self.frame.result_grid.GetNumberCols() > 0:
            delete_cols(self.frame.result_grid)

        # Reload Rows in case the Dataset Changed
        if self.frame.result_grid.GetNumberRows() > 0:
            self.frame.result_grid.DeleteRows(0, self.frame.result_grid.GetNumberRows())
            for i in range(self.frame.many_valued_grid.GetNumberRows()):
                self.frame.result_grid.AppendRows(1)
                self.frame.result_grid.SetRowLabelValue(i, self.frame.many_valued_grid.GetRowLabelValue(i))

        for i in range(len(self.datastorage.table.col_labels), -1, -1):
            self.get_apply_attribute(i)()

    def get_apply_attribute(self, col):
        def apply_attribute(evt=None):
            # Append Scaling Attributes of Single Dataset Attribute to the Result Grid

            if self.frame.many_valued_grid.GetColLabelValue(col) not in self.datastorage.table.scalings:
                return
            scaling = self.datastorage.table.scalings[self.frame.many_valued_grid.GetColLabelValue(col)]
            row_labels = scaling[0]
            col_labels = scaling[1]
            scaling_table = scaling[2]

            # Generate Column Labels
            col_offset = self.frame.result_grid.GetNumberCols()
            self.frame.result_grid.AppendCols(len(col_labels))
            for new_col in range(len(col_labels)):
                self.frame.result_grid.SetColLabelValue(col_offset + new_col, self.frame.many_valued_grid.GetColLabelValue(col) + ": " + col_labels[new_col])

            # Fill in Cells from Dataset
            for i in range(self.frame.many_valued_grid.GetNumberRows()):
                if self.frame.many_valued_grid.GetCellValue(i, col) != "":
                    value = self.frame.many_valued_grid.GetCellValue(i, col)
                    for j in range(len(col_labels)):
                        self.frame.result_grid.SetCellValue(i, col_offset + j, scaling_table[(row_labels.index(value), j)])

        return apply_attribute

    def get_rescale(self, scaling_type):
        def rescale(evt=None):
            # Recalculates scaling of currently opened tab
            attribute = self.current_grid.GetCornerLabelValue()
            col = 0
            for i in range(self.frame.many_valued_grid.GetNumberCols()):
                if self.frame.many_valued_grid.GetColLabelValue(i) == attribute:
                    col = i
                    break
            self.get_delete_selected_scaling(attribute)()
            self.get_to_scaling(col, scaling_type)()

        return rescale

    def get_to_scaling(self, col=None, scaling_type=None):
        def to_scaling(evt=None):

            # Load Scaling from Storage if it is Selected in Case Result is Visible
            if self.current_grid.GetCornerLabelValue() in self.datastorage.table.scalings:
                self.load_from_storage(self.current_grid.GetCornerLabelValue())
                self.datastorage.result_visible.discard(self.current_grid.GetCornerLabelValue())
                return

            # Add New Header if Scaling does not Exist
            self.get_save_to_storage(self.frame.scaling_tabs.GetSelection())()

            self.s.new_tab(self.frame.many_valued_grid.GetColLabelValue(col))
            attribute = self.frame.many_valued_grid.GetColLabelValue(col)
            self.current_grid.SetCornerLabelValue(attribute)

            # Generate Scaling Based on Selected Type

            if scaling_type == constants.EMPTY:
                # Ascertain Values
                values = list()
                for i in range(self.frame.many_valued_grid.GetNumberRows()):
                    if self.frame.many_valued_grid.GetCellValue(i, col) not in values:
                        if self.frame.many_valued_grid.GetCellValue(i, col) != "":
                            values.append(self.frame.many_valued_grid.GetCellValue(i, col))
                # Add Attribute Labels to Table
                delete_cols(self.current_grid)
                self.current_grid.DeleteRows(0, self.current_grid.GetNumberRows())
                self.current_grid.AppendCols(len(values))
                self.current_grid.AppendRows(len(values))
                for i in range(self.current_grid.GetNumberRows()):
                    self.current_grid.SetColLabelValue(i, values[i])
                    self.current_grid.SetRowLabelValue(i, values[i])

            if scaling_type == constants.NOMINAL or scaling_type == constants.ORDINAL:

                # Add Attribute Labels to Table
                columns_actual = self.s.get_col_entries(col, attribute)
                delete_cols(self.current_grid)
                self.current_grid.AppendCols(len(columns_actual))
                self.current_grid.DeleteRows(0, self.frame.many_valued_grid.GetNumberRows())
                self.current_grid.AppendRows(len(columns_actual))
                for a in range(len(columns_actual)):
                    self.current_grid.SetColLabelValue(a, str(columns_actual[a]))
                    self.current_grid.SetRowLabelValue(a, str(columns_actual[a]))

                # Fill Cells
                for i in range(self.current_grid.GetNumberRows()):
                    row_value = self.current_grid.GetRowLabelValue(i)
                    for j in range(self.current_grid.GetNumberCols()):
                        col_value = self.current_grid.GetColLabelValue(j)
                        if scaling_type == constants.ORDINAL and columns_actual.index(row_value) >= columns_actual.index(col_value):
                            self.current_grid.SetCellValue(i, j, "✘")
                        if scaling_type == constants.NOMINAL:
                            if row_value == col_value:
                                self.current_grid.SetCellValue(i, j, "✘")

            if scaling_type == constants.INTERORDINAL:

                columns_actual = self.s.get_col_entries(col, attribute)
                delete_cols(self.current_grid)
                self.current_grid.AppendCols(2*len(columns_actual))
                self.current_grid.DeleteRows(0, self.frame.many_valued_grid.GetNumberRows())
                self.current_grid.AppendRows(len(columns_actual))

                # Add Attribute Labels and Cells
                for a in range(2*(len(columns_actual))):
                    if a < len(columns_actual):
                        self.current_grid.SetColLabelValue(a, "≤" + str(columns_actual[a]))
                    else:
                        self.current_grid.SetColLabelValue(a, "≥" + str(columns_actual[a - len(columns_actual)]))
                for i in range(self.current_grid.GetNumberRows()):
                    self.current_grid.SetRowLabelValue(i, str(columns_actual[i]))
                    for j in range(i, i+(len(columns_actual)+1)):
                        self.current_grid.SetCellValue(i, j, "✘")

            self.current_grid.EnableEditing(False)
            self.frame.scaling_tabs.SetSelection(len(self.datastorage.grid_tabs) - 1)

        return to_scaling

    def view_result(self, evt=None):
        # Displays Result in Tab of Selected Scaling
        self.get_save_to_storage(self.frame.scaling_tabs.GetSelection())()
        self.current_grid = self.datastorage.grid_tabs[self.frame.scaling_tabs.GetSelection()]
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

            # Get Value of Object from Main Table and Check Scaling for Relation of the Value to the Attributes
            if self.datastorage.table.original[(i, col_number)] != "":
                value = self.datastorage.table.original[(i, col_number)]
                for j in range(len(scaling_col_labels)):
                    self.current_grid.SetCellValue(i, j, scaling_table[scaling_row_labels.index(value), j])

        self.datastorage.result_visible.add(self.current_grid.GetCornerLabelValue())
        self.frame.scaling_tabs.SetPageText(self.frame.scaling_tabs.GetSelection(), "Result:" + self.current_grid.GetCornerLabelValue())

    def get_save_to_storage(self, evt=None):
        def save_to_storage(evt=None):
            # -----Called When Tab Changes-----
            # Saves the Original Table, as well as the Currently Selected One, Unless the Result is Displayed

            self.current_grid = self.datastorage.grid_tabs[self.frame.scaling_tabs.GetSelection()]

            # Save Original Table
            self.datastorage.table.col_labels.clear()
            self.datastorage.table.row_labels.clear()
            self.datastorage.table.original.clear()

            for a in range(self.frame.many_valued_grid.GetNumberCols()):
                self.datastorage.table.col_labels.append(self.frame.many_valued_grid.GetColLabelValue(a))
            for b in range(self.frame.many_valued_grid.GetNumberRows()):
                self.datastorage.table.row_labels.append(self.frame.many_valued_grid.GetRowLabelValue(b))

            for i in range(self.frame.many_valued_grid.GetNumberRows()):
                for j in range(self.frame.many_valued_grid.GetNumberCols()):
                    self.datastorage.table.original[(i, j)] = self.frame.many_valued_grid.GetCellValue(i, j)

            # Save Current Scaling
            if self.frame.scaling_tabs.GetSelection() >= 2 and self.current_grid.GetCornerLabelValue() not in self.datastorage.result_visible:

                row_labels = list()
                col_labels = list()
                scaling_grid = self.datastorage.grid_tabs[self.frame.scaling_tabs.GetSelection()]
                for a in range(scaling_grid.GetNumberRows()):
                    row_labels.append(scaling_grid.GetRowLabelValue(a))
                for b in range(scaling_grid.GetNumberCols()):
                    col_labels.append(scaling_grid.GetColLabelValue(b))

                table = dict()
                for i in range(scaling_grid.GetNumberRows()):
                    for j in range(scaling_grid.GetNumberCols()):
                        table[(i, j)] = scaling_grid.GetCellValue(i, j)

                self.datastorage.table.set_scaling(scaling_grid.GetCornerLabelValue(), row_labels, col_labels, table)
            self.current_grid = self.datastorage.grid_tabs[self.frame.scaling_tabs.GetSelection()]
            self.update_result_grid()
        return save_to_storage

    def table_edited(self):
        # Save All Tables and Resets Scalings to Account for Table Changes
        # Called whenever changes are made to a table
        for i in range(len(self.datastorage.grid_tabs)):
            self.get_save_to_storage(i)()
            if i >= 2:
                self.current_grid = self.datastorage.grid_tabs[i]
                self.get_to_scaling(scaling_type=None)()
        self.current_grid = self.datastorage.grid_tabs[self.frame.scaling_tabs.GetSelection()]
        self.update_result_grid()
        self.sservice.update_all()

    def transfer_bins(self, attribute, ranges, scaling_type):
        # Recalculates Scaling based on Bin subdivision from statistics tab.
        # Called from stats panel

        scaling_grid = None
        for i in range(self.frame.scaling_tabs.GetPageCount()):
            if self.frame.scaling_tabs.GetPage(i).GetCornerLabelValue() == attribute:
                scaling_grid = self.frame.scaling_tabs.GetPage(i)

        delete_cols(scaling_grid)

        if scaling_type == constants.NOMINAL or scaling_type == constants.ORDINAL:
            for j in range(len(ranges)):
                scaling_grid.AppendCols(1)

                lim_low = str(ranges[j][0])
                lim_high = str(ranges[j][1])

                if len(lim_low) > 5:
                    lim_low = lim_low[0:5] + "..."
                if len(lim_high) > 5:
                    lim_high = lim_high[0:5] + "..."

                scaling_grid.SetColLabelValue(j, lim_low + " - " + lim_high)

            if scaling_type == constants.NOMINAL or scaling_type == constants.ORDINAL:
                for i in range(scaling_grid.GetNumberRows()):
                    row_value = float(scaling_grid.GetRowLabelValue(i))
                    for j in range(scaling_grid.GetNumberCols()):
                        if scaling_type == constants.ORDINAL and row_value <= ranges[j][1]:
                            scaling_grid.SetCellValue(i, j, "✘")
                        if scaling_type == constants.NOMINAL:
                            if ranges[j][1] >= row_value >= ranges[j][0]:
                                scaling_grid.SetCellValue(i, j, "✘")

        if scaling_type == constants.INTERORDINAL:
            for j in range(2*len(ranges)):
                scaling_grid.AppendCols(1)
                if j < len(ranges):
                    lim_low = str(ranges[j][0])
                    lim_high = str(ranges[j][1])

                    if len(lim_low) > 5:
                        lim_low = lim_low[0:5] + "..."
                    if len(lim_high) > 5:
                        lim_high = lim_high[0:5] + "..."
                    scaling_grid.SetColLabelValue(j, "≤" + lim_low + " - " + lim_high)
                else:
                    lim_low = str(ranges[j - len(ranges)][0])
                    lim_high = str(ranges[j - len(ranges)][1])

                    if len(lim_low) > 5:
                        lim_low = lim_low[0:5] + "..."
                    if len(lim_high) > 5:
                        lim_high = lim_high[0:5] + "..."
                    scaling_grid.SetColLabelValue(j, "≥" + lim_low + " - " + lim_high)

            for i in range(scaling_grid.GetNumberRows()):
                row_value = float(scaling_grid.GetRowLabelValue(i))
                for j in range(scaling_grid.GetNumberCols()):
                    if j < len(ranges):
                        if row_value <= ranges[j][1]:
                            scaling_grid.SetCellValue(i, j, "✘")
                    else:
                        if row_value >= ranges[j - len(ranges)][0]:
                            scaling_grid.SetCellValue(i, j, "✘")

    def transfer_partial_order(self, attribute, scaling_type, comparator):
        # Recalculates scaling based on partial order defined in statistics tab
        # Called from stats tab

        scaling_grid = None
        for i in range(self.frame.scaling_tabs.GetPageCount()):
            if self.frame.scaling_tabs.GetPage(i).GetCornerLabelValue() == attribute:
                scaling_grid = self.frame.scaling_tabs.GetPage(i)

        scaling_grid.ClearGrid()

        if scaling_type == constants.ORDINAL:

            for i in range(scaling_grid.GetNumberRows()):
                row_value = scaling_grid.GetRowLabelValue(i)
                for j in range(scaling_grid.GetNumberCols()):
                    col_value = self.current_grid.GetColLabelValue(j)
                    if comparator(row_value, col_value):
                        scaling_grid.SetCellValue(i, j, "✘")

        if scaling_type == constants.INTERORDINAL:

            cols = list()
            for i in range(scaling_grid.GetNumberCols()):
                cols.append(scaling_grid.GetColLabelValue(i))

            delete_cols(scaling_grid)

            for j in range(2*len(cols)):
                scaling_grid.AppendCols(1)
                if j < len(cols):
                    scaling_grid.SetColLabelValue(j, "≤" + str(cols[j]))
                else:
                    scaling_grid.SetColLabelValue(j, "≥" + str(cols[j - len(cols)]))

            for i in range(scaling_grid.GetNumberRows()):
                row_value = scaling_grid.GetRowLabelValue(i)
                for j in range(scaling_grid.GetNumberCols()):
                    if j < len(cols):
                        if comparator(row_value, cols[j]):
                            scaling_grid.SetCellValue(i, j, "✘")
                    else:
                        if comparator(cols[j - len(cols)], row_value):
                            scaling_grid.SetCellValue(i, j, "✘")

        self.get_save_to_storage()()

    def load_from_storage(self, target):
        # Loads Specified Table from Storage

        self.current_grid.DeleteRows(0, self.current_grid.GetNumberRows())
        delete_cols(self.current_grid)

        # Load Original
        if target == constants.ORIGINAL:

            self.frame.many_valued_grid.AppendCols(len(self.datastorage.table.col_labels))
            for a in range(len(self.datastorage.table.col_labels)):
                self.frame.many_valued_grid.SetColLabelValue(a, self.datastorage.table.col_labels[a])
            self.frame.many_valued_grid.AppendRows(len(self.datastorage.table.row_labels))
            for b in range(len(self.datastorage.table.row_labels)):
                self.frame.many_valued_grid.SetRowLabelValue(b, self.datastorage.table.row_labels[b])
            for coords, value in self.datastorage.table.original.items():
                self.frame.many_valued_grid.SetCellValue(coords[0], coords[1], value)
            self.current_grid = self.datastorage.grid_tabs[self.frame.scaling_tabs.GetSelection()]
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
        self.frame.scaling_tabs.SetPageText(self.datastorage.grid_tabs.index(self.current_grid), "Scale:" + target)
        self.current_grid = self.datastorage.grid_tabs[self.frame.scaling_tabs.GetSelection()]

    def check_toggle(self, evt):
        # Toggles Selection of Scaling Cells, if a scaling tab is currently selected
        if self.frame.scaling_tabs.GetSelection() >= 2 and self.s.current_attribute() not in self.datastorage.result_visible:
            self.current_grid = self.datastorage.grid_tabs[self.frame.scaling_tabs.GetSelection()]
            if self.current_grid.GetCellValue(evt.GetRow(), evt.GetCol()) == "":
                self.current_grid.SetCellValue(evt.GetRow(), evt.GetCol(), "✘")
            else:
                self.current_grid.SetCellValue(evt.GetRow(), evt.GetCol(), "")
            self.get_save_to_storage()()
            self.update_result_grid()
        else:
            evt.Skip()

    def get_delete_selected_scaling(self, attribute):
        def delete_selected_scaling(evt=None):

            if attribute in self.datastorage.table.scalings:
                for i in range(self.frame.scaling_tabs.GetPageCount()):
                    print(self.frame.scaling_tabs.GetPageText(0))
                    print(i)
                    if self.frame.scaling_tabs.GetPageText(i) == "Scale:" + attribute or self.frame.scaling_tabs.GetPageText(i) == "Result:" + attribute:
                        self.frame.scaling_tabs.DeletePage(i)
                        self.frame.scaling_tabs.SendSizeEvent()
                        self.datastorage.grid_tabs.pop(i)
                        break
                self.datastorage.table.scalings.pop(attribute)
                self.frame.scaling_tabs.SetSelection(0)

        return delete_selected_scaling

    def clear_scalings(self):
        # Deletes All Scalings and Related Data
        self.datastorage.result_visible.clear()
        self.datastorage.table.scalings.clear()
        while len(self.datastorage.grid_tabs) > 2:
            self.datastorage.grid_tabs.pop()

        while self.frame.scaling_tabs.GetPageCount() > 2:
            self.frame.scaling_tabs.DeletePage(2)

    def cell_changed(self, evt):
        # Called Whenever a Cell's Content Changes

        self.datastorage.set_edited()
        if self.frame.scaling_tabs.GetSelection() == 0:
            value = self.frame.many_valued_grid.GetCellValue(evt.GetRow(), evt.GetCol())
            attribute = self.frame.many_valued_grid.GetColLabelValue(evt.GetCol())

            # Update Level of Measurement if new Value is String
            try:
                float(value)
            except:
                if self.datastorage.table.attribute_levels[attribute] == constants.LEVEL_INT \
                            or self.datastorage.table.attribute_levels[attribute] == constants.LEVEL_RAT:
                    self.get_set_level(evt.GetCol(), attribute, constants.LEVEL_ORD)()

            # Update Scaling if Value is New
            if not self.s.value_in_scaling(value, attribute):
                scaling_rows = self.datastorage.table.scalings[attribute][0]
                scaling_cols = self.datastorage.table.scalings[attribute][1]
                scaling_table = self.datastorage.table.scalings[attribute][2]
                scaling_rows.append(value)
                for i in range(len(scaling_cols)):
                    scaling_table[len(scaling_rows)-1, i] = ""
                self.datastorage.table.set_scaling(attribute, scaling_rows, scaling_cols, scaling_table)
                self.datastorage.result_visible.discard(attribute)

                # Ascertain Table of Scaling. Current Grid Will be Reset by load_from_storage()
                for tab in self.datastorage.grid_tabs:
                    if tab.GetCornerLabelValue() == attribute:
                        self.current_grid = tab
                self.load_from_storage(attribute)

                errortext = 'The Value has been Added to the Scaling.'
                dialog = wx.MessageDialog(None, errortext, 'Entered Value is not Part of the Attributes Scaling', wx.ICON_WARNING | wx.OK)
                dialog.ShowModal()
        self.sservice.update_stats(evt=evt)

    def get_draw_lattice(self, draw_type, evt=None):
        def draw_lattice(evt=None):

            wx.BeginBusyCursor()
            objects, attributes, incidence = get_grid_data(self.current_grid)

            try:

                lattice = api.request_lattice_layout(self.mservice.api_address, objects, attributes, incidence, draw_type)
            except:
                menuservice.connection_error_dialog()
                wx.EndBusyCursor()
                return

            self.datastorage.lattice = lattice['layout']['result']
            self.gservice.create_lattice_graph()
            wx.EndBusyCursor()

        return draw_lattice



