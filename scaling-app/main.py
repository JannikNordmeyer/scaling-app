import wx
import wx.grid as grid
import menuservice
import concepts
import implications
import rules

def RowMenu(evt):

    menu = wx.Menu()
    delrow = menu.Append(wx.ID_ANY, "Delete Row")
    clearrow = menu.Append(wx.ID_ANY, "Clear Row")
    new = menu.Append(wx.ID_ANY, "Add Row")

    frame.Bind(wx.EVT_MENU, service.getDeleteRow(evt), delrow)
    frame.Bind(wx.EVT_MENU, service.getCleareRow(evt), clearrow)
    frame.Bind(wx.EVT_MENU, service.getAddRow(evt), new)

    frame.PopupMenu(menu)
    menu.Destroy()

def ColMenu(evt):

    menu = wx.Menu()
    delcol = menu.Append(wx.ID_ANY, "Delete Column")
    clearcol = menu.Append(wx.ID_ANY, "Clear Column")
    edit = menu.Append(wx.ID_ANY, "Edit Label")
    new = menu.Append(wx.ID_ANY, "Add Column")

    frame.Bind(wx.EVT_MENU, service.getDeleteCol(evt), delcol)
    frame.Bind(wx.EVT_MENU, service.getCleareCol(evt), clearcol)
    frame.Bind(wx.EVT_MENU, service.getEditLabel(evt), edit)
    frame.Bind(wx.EVT_MENU, service.getAddCol(evt), new)

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
    frame.Bind(wx.EVT_MENU, service.loadData, fileLoad)
    frame.Bind(wx.EVT_MENU, service.saveData, fileSave)
    frame.Bind(wx.EVT_MENU, service.emptyFrame, fileQuit)

    helpMenu = wx.Menu()
    helpAbout = helpMenu.Append(wx.ID_ANY, 'About', 'About')
    helpManual = helpMenu.Append(wx.ID_ANY, 'Manual', 'Manual')
    MenuBar.Append(helpMenu, 'Help')
    frame.Bind(wx.EVT_MENU, service.about, helpAbout)
    frame.Bind(wx.EVT_MENU, service.manual, helpManual)

    compMenu = wx.Menu()
    compConcepts = compMenu.Append(wx.ID_ANY, 'Compute Concepts', 'Compute Concepts')
    compImplications = compMenu.Append(wx.ID_ANY, 'Compute Implications', 'Compute Implications')
    compRules = compMenu.Append(wx.ID_ANY, 'Compute Rules', 'Compute Rules')
    MenuBar.Append(compMenu, 'Compute')
    frame.Bind(wx.EVT_MENU, service.compConcepts, compConcepts)
    frame.Bind(wx.EVT_MENU, service.compImplications, compImplications)
    frame.Bind(wx.EVT_MENU, service.compRules, compRules)

    quitMenu = wx.Menu()
    quitQuitScaling = quitMenu.Append(wx.ID_EXIT, 'Quit Scaling', 'Quit Scaling')
    MenuBar.Append(quitMenu, 'Quit Scaling')
    frame.Bind(wx.EVT_MENU, service.quitScaling, quitQuitScaling)

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

    frame.tabpane = wx.BoxSizer()
    frame.tabs = wx.Notebook(frame.panelBottom)
    tab1 = concepts.Concepts(frame.tabs)
    tab2 = implications.Implications(frame.tabs)
    tab3 = rules.Rules(frame.tabs)
    frame.tabs.AddPage(tab1, "Concepts")
    frame.tabs.AddPage(tab2, "Implications")
    frame.tabs.AddPage(tab3, "Rules")

    frame.grid.Bind(grid.EVT_GRID_LABEL_RIGHT_CLICK, LabelMenu)

    frame.csvbox.Add(frame.grid, wx.ID_ANY, wx.EXPAND)
    frame.panelTop.SetSizer(frame.csvbox)

    frame.tabpane.Add(frame.tabs, wx.ID_ANY, wx.EXPAND)
    frame.panelBottom.SetSizer(frame.tabpane)

app = wx.App()
frame = wx.Frame(None, title='FCA', size=(1200, 750))
frame.Center()
service = menuservice.menuService(frame)
buildUI(frame)
frame.Show()
app.MainLoop()

