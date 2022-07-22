import json
import wx
import tkinter.filedialog


def quit_scaling(e):
    exit(0)


class MenuService:

    def __init__(self, frame, datastorage, tableservice, graphservice):
        self.frame = frame
        self.datastorage = datastorage
        self.tableservice = tableservice
        self.graphservice = graphservice

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
        try:
            self.graphservice.draw_lattice()
        except:
            errortext = 'An error has occurred loading the context from the selected file. The file may be poorly formatted, or not contain a formal context lattice.'
            dialog = wx.MessageDialog(None, errortext, 'Error Loading Context', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            self.datastorage.context = storage_backup

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
