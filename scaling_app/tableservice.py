import csv
import wx


class tableservice:

    def __init__(self, frame, datastorage):
        self.frame = frame
        self.datastorage = datastorage

    def fillTable(self):

        values = csv.reader(self.datastorage.data, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)

        self.frame.grid.DeleteRows(0, self.frame.grid.GetNumberRows())
        self.frame.grid.DeleteCols(0, self.frame.grid.GetNumberCols())
        self.frame.grid.AppendRows(values.line_num)

        for row in values:

            if values.line_num == 1:
                self.frame.grid.AppendCols(len(row))
                i = 0
                for entry in row:
                    self.frame.grid.SetColLabelValue(i, entry)
                    i += 1
            else:
                self.frame.grid.AppendRows(1)
                j = 0
                for entry in row:
                    self.frame.grid.SetCellValue(values.line_num - 2, j, entry)
                    j += 1

    def getDeleteRow(self, labelEvent):
        def deleteRow(evt):
            self.frame.grid.DeleteRows(pos=labelEvent.GetRow(), updateLabels=False)

        return deleteRow

    def getCleareRow(self, labelEvent):
        def clearRow(evt):
            for i in range(self.frame.grid.GetNumberCols()):
                self.frame.grid.SetCellValue(labelEvent.GetRow(), i, "")

        return clearRow

    def getAddRow(self, labelevent):
        def addRow(evt):
            self.frame.grid.AppendRows()
            self.cascadeRow(labelevent.GetRow())

        return addRow

    def getDeleteCol(self, labelEvent):
        def deleteCol(evt):
            self.frame.grid.DeleteCols(pos=labelEvent.GetCol(), updateLabels=False)

        return deleteCol

    def getCleareCol(self, labelEvent):
        def clearCol(evt):
            for i in range(self.frame.grid.GetNumberRows()):
                self.frame.grid.SetCellValue(i, labelEvent.GetCol(), "")

        return clearCol

    def getEditLabel(self, labelevent):
        def editLabel(evt):
            dialog = wx.TextEntryDialog(None, "Column name:", caption="New Column", value="",
                                        style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
            dialog.ShowModal()
            name = dialog.GetValue()
            dialog.Destroy()
            if name != "":
                self.frame.grid.SetColLabelValue(labelevent.GetCol(), name)

        return editLabel

    def getAddCol(self, labelevent):
        def addCol(evt):
            dialog = wx.TextEntryDialog(None, "Column name:", caption="New Column", value="",
                                        style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
            dialog.ShowModal()
            name = dialog.GetValue()
            dialog.Destroy()
            if name != "":
                self.frame.grid.AppendCols()
                self.frame.grid.SetColLabelValue(self.frame.grid.GetNumberCols()-1, name)
                self.cascadeCol(labelevent.GetCol())

        return addCol


    def cascadeRow(self, pos):
        numberRows = self.frame.grid.GetNumberRows()
        i = 0
        while i < numberRows - pos - 2:
            self.swapRow(numberRows-2 - i, numberRows-1 - i)
            i += 1

    def swapRow(self, a, b):
        for i in range(self.frame.grid.GetNumberCols()):

            temp = self.frame.grid.GetCellValue(a, i)
            self.frame.grid.SetCellValue(a, i, self.frame.grid.GetCellValue(b, i))
            self.frame.grid.SetCellValue(b, i, temp)

    def cascadeCol(self, pos):
        numberCols = self.frame.grid.GetNumberCols()
        i = 0
        while i < numberCols - pos - 2:
            self.swapCol(numberCols-2 - i, numberCols-1 - i)
            i += 1

    def swapCol(self, a, b):

        temp = self.frame.grid.GetColLabelValue(a)
        self.frame.grid.SetColLabelValue(a, self.frame.grid.GetColLabelValue(b))
        self.frame.grid.SetColLabelValue(b, temp)
        for i in range(self.frame.grid.GetNumberRows()):

            temp = self.frame.grid.GetCellValue(i, a)
            self.frame.grid.SetCellValue(i, a, self.frame.grid.GetCellValue(i, b))
            self.frame.grid.SetCellValue(i, b, temp)
