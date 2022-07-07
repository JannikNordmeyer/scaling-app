import wx
import wx.grid as grid
import tkinter
import csv
from tkinter.filedialog import askopenfilename


def loadData(e):

    tkinter.Tk().withdraw()
    filePath = askopenfilename()
    print(filePath)
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
    print("Save Data")


def emptyFrame(e):
    print("Empty Frame")


def manual(e):
    print("Manual")


def about(e):
    print("About")


def quitScaling(e):
    exit(0)


def buildUI(frame):

    MenuBar = wx.MenuBar()

    fileMenu = wx.Menu()
    fileLoad = fileMenu.Append(wx.ID_FILE1, 'Load Data', 'Load Data')
    fileSave = fileMenu.Append(wx.ID_FILE2, 'Save Data', 'Save Data')
    fileMenu.AppendSeparator()
    fileQuit = fileMenu.Append(wx.ID_FILE3, 'Empty Frame', 'Empty Frame')
    MenuBar.Append(fileMenu, 'Data')
    frame.Bind(wx.EVT_MENU, loadData, fileLoad)
    frame.Bind(wx.EVT_MENU, saveData, fileSave)
    frame.Bind(wx.EVT_MENU, emptyFrame, fileQuit)

    helpMenu = wx.Menu()
    helpAbout = helpMenu.Append(wx.ID_ABOUT, 'About', 'About')
    helpManual = helpMenu.Append(wx.ID_HELP, 'Manual', 'Manual')
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

    frame.csvbox.Add(frame.grid, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)
    frame.panelTop.SetSizer(frame.csvbox)



app = wx.App()
frame = wx.Frame(None, title='FCA', size=(1200, 750))
frame.Center()
buildUI(frame)
frame.Show()
app.MainLoop()

