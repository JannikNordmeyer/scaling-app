import json
import wx
import tkinter.filedialog


class MenuService:

    def __init__(self, frame, datastorage, tableservice, graphservice):
        self.frame = frame
        self.datastorage = datastorage
        self.tableservice = tableservice
        self.graphservice = graphservice

    def show_row_menu(self, evt):

        menu = wx.Menu()
        delrow = menu.Append(wx.ID_ANY, "Delete Row")
        clearrow = menu.Append(wx.ID_ANY, "Clear Row")
        new = menu.Append(wx.ID_ANY, "Add Row")

        self.frame.Bind(wx.EVT_MENU, self.tableservice.get_delete_row(evt), delrow)
        self.frame.Bind(wx.EVT_MENU, self.tableservice.get_clear_row(evt), clearrow)
        self.frame.Bind(wx.EVT_MENU, self.tableservice.get_add_row(evt), new)

        self.frame.PopupMenu(menu)
        menu.Destroy()

    def show_col_menu(self, evt):

        menu = wx.Menu()
        delcol = menu.Append(wx.ID_ANY, "Delete Column")
        clearcol = menu.Append(wx.ID_ANY, "Clear Column")
        edit = menu.Append(wx.ID_ANY, "Edit Label")
        new = menu.Append(wx.ID_ANY, "Add Column")

        self.frame.Bind(wx.EVT_MENU, self.tableservice.get_delete_col(evt), delcol)
        self.frame.Bind(wx.EVT_MENU, self.tableservice.get_clear_col(evt), clearcol)
        self.frame.Bind(wx.EVT_MENU, self.tableservice.get_edit_label(evt), edit)
        self.frame.Bind(wx.EVT_MENU, self.tableservice.get_add_col(evt), new)

        self.frame.PopupMenu(menu)
        menu.Destroy()

    def label_menu(self, evt):

        evt.Skip()
        if evt.GetCol() == -1:
            self.show_row_menu(evt)
        else:
            self.show_col_menu(evt)

    def cell_menu(self, evt):
        menu = wx.Menu()
        clear = menu.Append(wx.ID_ANY, "Clear Table")
        reset = menu.Append(wx.ID_ANY, "Reset Table")

        self.frame.Bind(wx.EVT_MENU, self.tableservice.clear_table, clear)
        self.frame.Bind(wx.EVT_MENU, self.tableservice.reset_table, reset)

        self.frame.PopupMenu(menu)
        menu.Destroy()

    def graph_menu(self, evt):
        menu = wx.Menu()
        redraw = menu.Append(wx.ID_ANY, "Redraw Lattice")
        clear = menu.Append(wx.ID_ANY, "Clear Lattice")

        self.frame.Bind(wx.EVT_MENU, self.graphservice.redraw_lattice, redraw)
        self.frame.Bind(wx.EVT_MENU, self.graphservice.clear, clear)

        self.frame.PopupMenu(menu)
        menu.Destroy()

    def redraw(self, event):
        dc = wx.ClientDC(self.frame.panelLeft)
        dc.Clear()
        if self.datastorage.context is not None:
            self.graphservice.draw_lattice()
        event.Skip()

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
        storage_backup = self.datastorage.context
        self.datastorage.context = json.load(file)

        self.graphservice.draw_lattice()

    def save_data(self, e):

        tkinter.Tk().withdraw()
        filepath = tkinter.filedialog.asksaveasfilename(defaultextension=".csv")
        if filepath == "":
            return

        content = ""
        row_count = self.frame.grid.GetNumberRows()
        row_len = self.frame.grid.GetNumberCols()

        for labels in range(row_len):
            value = self.frame.grid.GetColLabelValue(labels)
            value = value.replace(",", "\,")
            content += value
            if labels < row_len - 1:
                content += ","
        content += "\n"

        for i in range(row_count):
            for j in range(row_len):

                value = self.frame.grid.GetCellValue(i, j)
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
        print("Manual")

    def about(self, e):
        print("About")

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
