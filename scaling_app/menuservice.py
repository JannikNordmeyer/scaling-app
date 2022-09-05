import json
import wx
import wx.grid as grid
import tkinter.filedialog
from scaling_app import constants


class MenuService:

    def __init__(self, frame, datastorage, tableservice, graphservice):
        self.frame = frame
        self.datastorage = datastorage
        self.tableservice = tableservice
        self.graphservice = graphservice

    def show_row_menu(self, evt):

        menu = wx.Menu()
        row_label = self.tableservice.current_grid.GetRowLabelValue(evt.GetRow())
        col = None
        if self.frame.csvtabs.GetSelection() > 0:
            selected_scaling = self.datastorage.tabs[self.frame.csvtabs.GetSelection()].GetCornerLabelValue()
            col = self.datastorage.table.col_labels.index(selected_scaling)

        if not self.tableservice.value_in_data(row_label, col):
            delrow = menu.Append(wx.ID_ANY, "Delete Object")
            self.frame.Bind(wx.EVT_MENU, self.tableservice.get_delete_row(evt), delrow)
            purgerow = menu.Append(wx.ID_ANY, "Purge Object")
            self.frame.Bind(wx.EVT_MENU, self.tableservice.get_purge_row(evt), purgerow)
            edit = menu.Append(wx.ID_ANY, "Edit Label")
            self.frame.Bind(wx.EVT_MENU, self.tableservice.get_edit_row_label(evt), edit)
        new = menu.Append(wx.ID_ANY, "Add Object")
        self.frame.Bind(wx.EVT_MENU, self.tableservice.get_add_row(evt), new)

        self.frame.PopupMenu(menu)
        menu.Destroy()

    def show_col_menu(self, evt):

        menu = wx.Menu()
        delcol = menu.Append(wx.ID_ANY, "Delete Attribute")
        purgecol = menu.Append(wx.ID_ANY, "Purge Attribute")
        edit = menu.Append(wx.ID_ANY, "Edit Label")
        new = menu.Append(wx.ID_ANY, "Add Attribute")
        self.frame.Bind(wx.EVT_MENU, self.tableservice.get_delete_col(evt), delcol)
        self.frame.Bind(wx.EVT_MENU, self.tableservice.get_purge_col(evt), purgecol)
        self.frame.Bind(wx.EVT_MENU, self.tableservice.get_edit_col_label(evt), edit)
        self.frame.Bind(wx.EVT_MENU, self.tableservice.get_add_col(evt), new)

        if self.frame.csvtabs.GetSelection() == 0:
            if self.frame.main_grid.GetColLabelValue(evt.GetCol()) not in self.datastorage.table.scalings and "\n" not in self.frame.main_grid.GetColLabelValue(evt.GetCol()):
                menu.AppendSeparator()
                scaling = wx.Menu()
                custom = scaling.Append(wx.ID_ANY, "Custom Scaling")
                self.frame.Bind(wx.EVT_MENU, self.tableservice.get_to_scaling(evt, constants.EMPTY), custom)
                if self.tableservice.check_int_col(evt.GetCol()):
                    nominal = scaling.Append(wx.ID_ANY, "Nominal Scaling")
                    ordinal = scaling.Append(wx.ID_ANY, "Ordinal Scaling")
                    interordinal = scaling.Append(wx.ID_ANY, "Interordinal Scaling")
                    self.frame.Bind(wx.EVT_MENU, self.tableservice.get_to_scaling(evt, constants.DIAGONAL), nominal)
                    self.frame.Bind(wx.EVT_MENU, self.tableservice.get_to_scaling(evt, constants.ORDINAL), ordinal)
                    self.frame.Bind(wx.EVT_MENU, self.tableservice.get_to_scaling(evt, constants.INTERORDINAL), interordinal)
                else:
                    nominal = scaling.Append(wx.ID_ANY, "Nominal Scaling")
                    self.frame.Bind(wx.EVT_MENU, self.tableservice.get_to_scaling(evt, constants.DIAGONAL_ANY), nominal)
                menu.Append(wx.ID_ANY, "Scale Attribute", scaling)

        self.frame.PopupMenu(menu)
        menu.Destroy()

    def label_menu(self, evt):
        print(evt.GetRow())
        print(evt.GetCol())
        evt.Skip()
        if evt.GetCol() == -1:
            self.show_row_menu(evt)
        else:
            self.show_col_menu(evt)

    def cell_menu(self, evt):

        menu = wx.Menu()
        purge = menu.Append(wx.ID_ANY, "Purge Table")
        reset = menu.Append(wx.ID_ANY, "Reset Table")
        menu.AppendSeparator()

        if self.frame.csvtabs.GetSelection() > 0 and "Scaling:" in self.frame.csvtabs.GetPageText(self.frame.csvtabs.GetSelection()):
            result = menu.Append(wx.ID_ANY, "View Result")
            self.frame.Bind(wx.EVT_MENU, self.tableservice.view_result, result)
        if self.frame.csvtabs.GetSelection() > 0 and "Result:" in self.frame.csvtabs.GetPageText(self.frame.csvtabs.GetSelection()):
            to_scaling = menu.Append(wx.ID_ANY, "Go to Scaling")
            self.frame.Bind(wx.EVT_MENU, self.tableservice.get_to_scaling(evt, None), to_scaling)
        if self.frame.csvtabs.GetSelection() > 0:
            menu.AppendSeparator()
            delete = menu.Append(wx.ID_ANY, "Delete Scaling")
            self.frame.Bind(wx.EVT_MENU, self.tableservice.get_delete_selected_scaling(self.tableservice.current_grid.GetCornerLabelValue()), delete)

        self.frame.Bind(wx.EVT_MENU, self.tableservice.purge_table, purge)
        self.frame.Bind(wx.EVT_MENU, self.tableservice.reset_table, reset)

        self.frame.PopupMenu(menu)
        menu.Destroy()

    def graph_menu(self):

        menu = wx.Menu()
        redraw = menu.Append(wx.ID_ANY, "Redraw Lattice")
        clear = menu.Append(wx.ID_ANY, "Clear Lattice")

        self.frame.Bind(wx.EVT_MENU, self.graphservice.draw_lattice, redraw)
        self.frame.Bind(wx.EVT_MENU, self.graphservice.clear, clear)

        self.frame.PopupMenu(menu)
        menu.Destroy()

    def load_data(self, e):

        tkinter.Tk().withdraw()
        filepath = tkinter.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath == "":
            return
        csvfile = open(filepath)
        storage_backup = self.datastorage.data
        self.datastorage.data = csvfile

        try:
            self.tableservice.fill_table()
            self.datastorage.clear_table()
            while self.frame.csvtabs.GetPageCount() > 2:
                self.frame.csvtabs.DeletePage(2)
            if self.frame.result_grid.GetNumberCols() > 0:
                self.frame.result_grid.DeleteCols(0, self.frame.result_grid.GetNumberCols())
            if self.frame.result_grid.GetNumberRows() > 0:
                self.frame.result_grid.DeleteRows(0, self.frame.result_grid.GetNumberRows())
            for i in range(self.frame.main_grid.GetNumberRows()):
                self.frame.result_grid.AppendRows(1)
                self.frame.result_grid.SetRowLabelValue(i, self.frame.main_grid.GetRowLabelValue(i))
        except:
            errortext = 'An error has occurred loading the context from the selected file. The file may be poorly formatted.'
            dialog = wx.MessageDialog(None, errortext, 'Error Loading Context', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            self.datastorage.data = storage_backup

    def load_lattice(self, e):

        tkinter.Tk().withdraw()
        filepath = tkinter.filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filepath == "":
            return
        file = open(filepath)
        storage_backup = self.datastorage.lattice
        self.datastorage.lattice = json.load(file)

        try:
            self.graphservice.draw_lattice()
        except:
            errortext = 'An error has occurred loading the lattice from the selected file. The file may be poorly formatted.'
            dialog = wx.MessageDialog(None, errortext, 'Error Loading Lattice', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            self.datastorage.lattice = storage_backup

    def save_data(self, e):

        tkinter.Tk().withdraw()
        filepath = tkinter.filedialog.asksaveasfilename(defaultextension=".csv")
        if filepath == "":
            return

        content = ""
        row_count = self.frame.main_grid.GetNumberRows()
        row_len = self.frame.main_grid.GetNumberCols()

        for labels in range(row_len):
            value = self.frame.main_grid.GetColLabelValue(labels)
            value = value.replace(",", "\,")
            content += value
            if labels < row_len - 1:
                content += ","
        content += "\n"

        for i in range(row_count):
            value = self.frame.main_grid.GetRowLabelValue(i)
            value = value.replace(",", "\,")
            value += ","
            content += value
            for j in range(row_len):

                value = self.frame.main_grid.GetCellValue(i, j)
                value = value.replace(",", "\,")
                content += value
                if j < row_len - 1:
                    content += ","
            content += "\n"

        f = open(filepath, "w")
        f.seek(0)
        f.write(content)
        f.truncate()
        f.close()
        self.datastorage.clear_edited()

    def empty_frame(self, e):
        print("Empty Frame")

    def manual(self, e):
        self.datastorage.status()

    def about(self, e):
        self.datastorage.status()

    def comp_concepts(self, e):
        print("Compute Concepts")

    def comp_implications(self, e):
        print("Compute Implications")

    def comp_rules(self, e):
        print("Compute Rules")

    def quit_scaling(self, e=None):
        if not self.datastorage.edited:
            exit(0)
        else:
            errortext = 'You have unsaved changes. Do you want to close the application regardless?'
            dialog = wx.MessageDialog(None, errortext, 'Data Loss Warning', wx.ICON_WARNING | wx.YES_NO)
            answer = dialog.ShowModal()
            if answer == wx.ID_YES:
                dialog.Destroy()
                exit(0)
