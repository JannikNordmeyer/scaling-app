import wx
import wx.grid as grid
from scaling_app import menuservice, tableservice, graphservice, datastorage
from scaling_app import concepts
from scaling_app import implications
from scaling_app import rules


def RowMenu(evt):

    menu = wx.Menu()
    delrow = menu.Append(wx.ID_ANY, "Delete Row")
    clearrow = menu.Append(wx.ID_ANY, "Clear Row")
    new = menu.Append(wx.ID_ANY, "Add Row")

    frame.Bind(wx.EVT_MENU, tservice.getDeleteRow(evt), delrow)
    frame.Bind(wx.EVT_MENU, tservice.getCleareRow(evt), clearrow)
    frame.Bind(wx.EVT_MENU, tservice.getAddRow(evt), new)

    frame.PopupMenu(menu)
    menu.Destroy()


def ColMenu(evt):

    menu = wx.Menu()
    delcol = menu.Append(wx.ID_ANY, "Delete Column")
    clearcol = menu.Append(wx.ID_ANY, "Clear Column")
    edit = menu.Append(wx.ID_ANY, "Edit Label")
    new = menu.Append(wx.ID_ANY, "Add Column")

    frame.Bind(wx.EVT_MENU, tservice.getDeleteCol(evt), delcol)
    frame.Bind(wx.EVT_MENU, tservice.getCleareCol(evt), clearcol)
    frame.Bind(wx.EVT_MENU, tservice.getEditLabel(evt), edit)
    frame.Bind(wx.EVT_MENU, tservice.getAddCol(evt), new)

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
    graphLoad = fileMenu.Append(wx.ID_ANY, 'Load Lattice', 'Load Lattice')
    fileSave = fileMenu.Append(wx.ID_ANY, 'Save Data', 'Save Data')
    fileMenu.AppendSeparator()
    fileQuit = fileMenu.Append(wx.ID_ANY, 'Empty Frame', 'Empty Frame')
    MenuBar.Append(fileMenu, 'Data')
    frame.Bind(wx.EVT_MENU, mservice.loadData, fileLoad)
    frame.Bind(wx.EVT_MENU, mservice.loadLattice, graphLoad)
    frame.Bind(wx.EVT_MENU, mservice.saveData, fileSave)
    frame.Bind(wx.EVT_MENU, mservice.emptyFrame, fileQuit)

    helpMenu = wx.Menu()
    helpAbout = helpMenu.Append(wx.ID_ANY, 'About', 'About')
    helpManual = helpMenu.Append(wx.ID_ANY, 'Manual', 'Manual')
    MenuBar.Append(helpMenu, 'Help')
    frame.Bind(wx.EVT_MENU, mservice.about, helpAbout)
    frame.Bind(wx.EVT_MENU, mservice.manual, helpManual)

    compMenu = wx.Menu()
    compConcepts = compMenu.Append(wx.ID_ANY, 'Compute Concepts', 'Compute Concepts')
    compImplications = compMenu.Append(wx.ID_ANY, 'Compute Implications', 'Compute Implications')
    compRules = compMenu.Append(wx.ID_ANY, 'Compute Rules', 'Compute Rules')
    MenuBar.Append(compMenu, 'Compute')
    frame.Bind(wx.EVT_MENU, mservice.compConcepts, compConcepts)
    frame.Bind(wx.EVT_MENU, mservice.compImplications, compImplications)
    frame.Bind(wx.EVT_MENU, mservice.compRules, compRules)

    quitMenu = wx.Menu()
    quitQuitScaling = quitMenu.Append(wx.ID_EXIT, 'Quit Scaling', 'Quit Scaling')
    MenuBar.Append(quitMenu, 'Quit Scaling')
    frame.Bind(wx.EVT_MENU, mservice.quitScaling, quitQuitScaling)

    frame.SetMenuBar(MenuBar)

    frame.hsplitter = wx.SplitterWindow(frame, style = wx.SP_LIVE_UPDATE)
    frame.vsplitter = wx.SplitterWindow(frame.hsplitter, style = wx.SP_LIVE_UPDATE)

    frame.panelLeft = wx.Panel(frame.hsplitter, wx.ID_ANY, style=wx.BORDER_SUNKEN)
    frame.panelTop = wx.Panel(frame.vsplitter, wx.ID_ANY, style=wx.BORDER_SUNKEN)
    frame.panelBottom = wx.Panel(frame.vsplitter, wx.ID_ANY, style=wx.BORDER_SUNKEN)

    frame.vsplitter.SplitHorizontally(frame.panelTop, frame.panelBottom)

    frame.hsplitter.SplitVertically(frame.panelLeft, frame.vsplitter)
    frame.hsplitter.SetMinimumPaneSize(100)
    frame.hsplitter.SetSashPosition(400)
    frame.hsplitter.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, mservice.redraw)
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
storage = datastorage.datastorage()
tservice = tableservice.tableservice(frame, storage)
gservice = graphservice.graphservice(frame, storage)
mservice = menuservice.menuService(frame, storage, tservice, gservice)
buildUI(frame)
frame.Show()
frame.Bind(wx.EVT_SIZE, mservice.redraw)
frame.Bind(wx.EVT_MOVE_END, mservice.redraw)
app.MainLoop()
