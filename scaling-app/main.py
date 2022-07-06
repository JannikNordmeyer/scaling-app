import wx

def loadData(e):
    print("Load Data")


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
    frame.listbox = wx.ListBox(frame.panelTop)

    frame.listbox.Append("Value A")
    frame.listbox.Append("Value B")
    frame.listbox.Append("Value C")
    frame.csvbox.Add(frame.listbox, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)
    frame.panelTop.SetSizer(frame.csvbox)


app = wx.App()
frame = wx.Frame(None, title='FCA', size=(1200, 750))
frame.Center()
buildUI(frame)
frame.Show()
app.MainLoop()

