import wx
import wx.grid as grid
import csv
import tkinter.filedialog


def loadData(e):

    tkinter.Tk().withdraw()
    filePath = tkinter.filedialog.askopenfilename()
    if filePath == "":
        return
    with open(filePath) as csvfile:

        values = csv.reader(csvfile, delimiter=',', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)

        frame.grid.DeleteRows(0, frame.grid.GetNumberRows())
        frame.grid.DeleteCols(0, frame.grid.GetNumberCols())
        frame.grid.AppendRows(values.line_num)

        for row in values:

            if values.line_num == 1:
                frame.grid.AppendCols(len(row))
                i = 0
                for entry in row:
                    frame.grid.SetColLabelValue(i, entry)
                    i += 1
            else:
                frame.grid.AppendRows(1)
                j = 0
                for entry in row:
                    frame.grid.SetCellValue(values.line_num - 2, j, entry)
                    j += 1

def saveData(e):

    tkinter.Tk().withdraw()
    filePath = tkinter.filedialog.asksaveasfilename(defaultextension=".csv")
    if filePath == "":
        return

    content = ""
    rowCount = frame.grid.GetNumberRows()
    rowLen = frame.grid.GetNumberCols()

    for labels in range(rowLen):
        value = frame.grid.GetColLabelValue(labels)
        value = value.replace(",", "\,")
        content += value
        if labels < rowLen-1:
            content += ","
    content += "\n"

    for i in range(rowCount):
        for j in range(rowLen):

            value = frame.grid.GetCellValue(i, j)
            value = value.replace(",", "\,")
            content += value
            if j < rowLen-1:
                content += ","
        content += "\n"

    f = open(filePath, "w")
    f.seek(0)
    f.write(content)
    f.truncate()
    f.close()




def emptyFrame(e):
    print("Empty Frame")


def manual(e):
    print("Manual")


def about(e):
    print("About")


def quitScaling(e):
    exit(0)

def deleteCol(evt, col):
    print("DeleteCol")

def getDeleteRow(labelEvent):
    def deleteRow(evt):
        frame.grid.DeleteRows(pos=labelEvent.GetRow(), updateLabels=False)
    return deleteRow

def getCleareRow(labelEvent):
    def clearRow(evt):
        for i in range(frame.grid.GetNumberCols()):
            frame.grid.SetCellValue(labelEvent.GetRow(), i, "")
    return clearRow

def getDeleteCol(labelEvent):
    def deleteCol(evt):
        frame.grid.DeleteCols(pos=labelEvent.GetCol(), updateLabels=False)
    return deleteCol

def getCleareCol(labelEvent):
    def clearCol(evt):
        for i in range(frame.grid.GetNumberRows()):
            frame.grid.SetCellValue(i, labelEvent.GetCol(), "")
    return clearCol

def getEditLabel(labelevent):
    def editLabel(evt):
        dialog = wx.TextEntryDialog(None, "Column name:", caption="New Column", value="", style=wx.TextEntryDialogStyle, pos=wx.DefaultPosition)
        dialog.ShowModal()
        name = dialog.GetValue()
        dialog.Destroy()
        frame.grid.SetColLabelValue(labelevent.GetCol(), name)

    return editLabel


def RowMenu(evt):

    menu = wx.Menu()
    delrow = menu.Append(wx.ID_ANY, "Delete Row")
    clearrow = menu.Append(wx.ID_ANY, "Clear Row")

    frame.Bind(wx.EVT_MENU, getDeleteRow(evt), delrow)
    frame.Bind(wx.EVT_MENU, getCleareRow(evt), clearrow)

    frame.PopupMenu(menu)
    menu.Destroy()

def ColMenu(evt):

    menu = wx.Menu()
    delcol = menu.Append(wx.ID_ANY, "Delete Column")
    clearcol = menu.Append(wx.ID_ANY, "Clear Column")
    edit = menu.Append(wx.ID_ANY, "Edit Label")

    frame.Bind(wx.EVT_MENU, getDeleteCol(evt), delcol)
    frame.Bind(wx.EVT_MENU, getCleareCol(evt), clearcol)
    frame.Bind(wx.EVT_MENU, getEditLabel(evt), edit)

    frame.PopupMenu(menu)
    menu.Destroy()

def LabelMenu(evt):

    evt.Skip()
    if evt.GetCol() == -1:
        RowMenu(evt)
    else:
        ColMenu(evt)

def buildUI(frame):

    MenuBar = wx.MenuBar()

    fileMenu = wx.Menu()
    fileLoad = fileMenu.Append(wx.ID_ANY, 'Load Data', 'Load Data')
    fileSave = fileMenu.Append(wx.ID_ANY, 'Save Data', 'Save Data')
    fileMenu.AppendSeparator()
    fileQuit = fileMenu.Append(wx.ID_ANY, 'Empty Frame', 'Empty Frame')
    MenuBar.Append(fileMenu, 'Data')
    frame.Bind(wx.EVT_MENU, loadData, fileLoad)
    frame.Bind(wx.EVT_MENU, saveData, fileSave)
    frame.Bind(wx.EVT_MENU, emptyFrame, fileQuit)

    helpMenu = wx.Menu()
    helpAbout = helpMenu.Append(wx.ID_ANY, 'About', 'About')
    helpManual = helpMenu.Append(wx.ID_ANY, 'Manual', 'Manual')
    MenuBar.Append(helpMenu, 'Help')
    frame.Bind(wx.EVT_MENU, about, helpAbout)
    frame.Bind(wx.EVT_MENU, manual, helpManual)

    quitMenu = wx.Menu()
    quitQuitScaling = quitMenu.Append(wx.ID_EXIT, 'Quit Scaling', 'Quit Scaling')
    MenuBar.Append(quitMenu, 'Quit Scaling')
    frame.Bind(wx.EVT_MENU, quitScaling, quitQuitScaling)

    frame.SetMenuBar(MenuBar)

    frame.hsplitter = wx.SplitterWindow(frame)
    frame.vsplitter = wx.SplitterWindow(frame.hsplitter)

    frame.panelLeft = wx.Panel(frame.hsplitter, wx.ID_ANY, style=wx.BORDER_SUNKEN)
    frame.panelTop = wx.Panel(frame.vsplitter, wx.ID_ANY, style=wx.BORDER_SUNKEN)
    frame.panelBottom = wx.Panel(frame.vsplitter, wx.ID_ANY, style=wx.BORDER_SUNKEN)

    frame.vsplitter.SplitHorizontally(frame.panelTop, frame.panelBottom)

    frame.hsplitter.SplitVertically(frame.panelLeft, frame.vsplitter)
    frame.hsplitter.SetMinimumPaneSize(100)
    frame.hsplitter.SetSashPosition(400)
    frame.vsplitter.SetMinimumPaneSize(100)
    frame.vsplitter.SetSashPosition(400)

    frame.csvbox = wx.BoxSizer(wx.VERTICAL)
    frame.grid = grid.Grid(frame.panelTop)
    frame.grid.CreateGrid(16, 8)
    frame.grid.EnableDragCell()
    frame.grid.EnableDragColMove()

    frame.grid.Bind(grid.EVT_GRID_LABEL_RIGHT_CLICK, LabelMenu)

    frame.csvbox.Add(frame.grid, wx.ID_ANY, wx.EXPAND)
    frame.panelTop.SetSizer(frame.csvbox)


app = wx.App()
frame = wx.Frame(None, title='FCA', size=(1200, 750))
frame.Center()
buildUI(frame)
frame.Show()
app.MainLoop()

