import json
import wx
import tkinter.filedialog


class menuService:

    def __init__(self, frame, datastorage, tableservice, graphservice):
        self.frame = frame
        self.datastorage = datastorage
        self.tableservice = tableservice
        self.graphservice = graphservice

    def redraw(self, event):
        dc = wx.ClientDC(self.frame.panelLeft)
        dc.Clear()
        if self.datastorage.context is not None:
            self.graphservice.drawLattice()
        event.Skip()

    def loadData(self, e):

        tkinter.Tk().withdraw()
        filePath = tkinter.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filePath == "":
            return
        csvfile = open(filePath)
        storagebackup = self.datastorage.data
        self.datastorage.data = csvfile
        try:
            self.tableservice.fillTable()
        except:
            errortext = 'An error has occurred loading the context from the selected file. The file may be poorly formatted.'
            dialog = wx.MessageDialog(None, errortext, 'Error Loading Context', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            self.datastorage.data = storagebackup

    def loadLattice(self, e):

        tkinter.Tk().withdraw()
        filePath = tkinter.filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filePath == "":
            return
        file = open(filePath)
        storagebackup = self.datastorage.context
        self.datastorage.context = json.load(file)
        try:
            self.graphservice.drawLattice()
        except:
            errortext = 'An error has occurred loading the context from the selected file. The file may be poorly formatted, or not contain a formal context lattice.'
            dialog = wx.MessageDialog(None, errortext, 'Error Loading Context', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            self.datastorage.context = storagebackup

    def saveData(self, e):

        tkinter.Tk().withdraw()
        filePath = tkinter.filedialog.asksaveasfilename(defaultextension=".csv")
        if filePath == "":
            return

        content = ""
        rowCount = self.frame.grid.GetNumberRows()
        rowLen = self.frame.grid.GetNumberCols()

        for labels in range(rowLen):
            value = self.frame.grid.GetColLabelValue(labels)
            value = value.replace(",", "\,")
            content += value
            if labels < rowLen - 1:
                content += ","
        content += "\n"

        for i in range(rowCount):
            for j in range(rowLen):

                value = self.frame.grid.GetCellValue(i, j)
                value = value.replace(",", "\,")
                content += value
                if j < rowLen - 1:
                    content += ","
            content += "\n"

        f = open(filePath, "w")
        f.seek(0)
        f.write(content)
        f.truncate()
        f.close()

    def emptyFrame(self, e):
        print("Empty Frame")

    def manual(self, e):
        print("Manual")

    def about(self, e):
        print("About")

    def quitScaling(self, e):
        exit(0)

    def compConcepts(self, e):
        print("Compute Concepts")

    def compImplications(self, e):
        print("Compute Implications")

    def compRules(self, e):
        print("Compute Rules")

