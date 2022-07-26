import wx
import wx.grid as grid
from scaling_app import menuservice, tableservice, graphservice, datastorage
from scaling_app import concepts
from scaling_app import implications
from scaling_app import rules


def build_ui():

    menu_bar = wx.MenuBar()

    file_menu = wx.Menu()
    file_load = file_menu.Append(wx.ID_ANY, 'Load Data', 'Load Data')
    graph_load = file_menu.Append(wx.ID_ANY, 'Load Lattice', 'Load Lattice')
    file_save = file_menu.Append(wx.ID_ANY, 'Save Data', 'Save Data')
    file_menu.AppendSeparator()
    file_quit = file_menu.Append(wx.ID_ANY, 'Empty Frame', 'Empty Frame')
    menu_bar.Append(file_menu, 'Data')
    frame.Bind(wx.EVT_MENU, mservice.load_data, file_load)
    frame.Bind(wx.EVT_MENU, mservice.load_lattice, graph_load)
    frame.Bind(wx.EVT_MENU, mservice.save_data, file_save)
    frame.Bind(wx.EVT_MENU, mservice.empty_frame, file_quit)

    help_menu = wx.Menu()
    help_about = help_menu.Append(wx.ID_ANY, 'About', 'About')
    help_manual = help_menu.Append(wx.ID_ANY, 'Manual', 'Manual')
    menu_bar.Append(help_menu, 'Help')
    frame.Bind(wx.EVT_MENU, mservice.about, help_about)
    frame.Bind(wx.EVT_MENU, mservice.manual, help_manual)

    comp_menu = wx.Menu()
    comp_concepts = comp_menu.Append(wx.ID_ANY, 'Compute Concepts', 'Compute Concepts')
    comp_implications = comp_menu.Append(wx.ID_ANY, 'Compute Implications', 'Compute Implications')
    comp_rules = comp_menu.Append(wx.ID_ANY, 'Compute Rules', 'Compute Rules')
    menu_bar.Append(comp_menu, 'Compute')
    frame.Bind(wx.EVT_MENU, mservice.comp_concepts, comp_concepts)
    frame.Bind(wx.EVT_MENU, mservice.comp_implications, comp_implications)
    frame.Bind(wx.EVT_MENU, mservice.comp_rules, comp_rules)

    quit_menu = wx.Menu()
    quit_quit_scaling = quit_menu.Append(wx.ID_EXIT, 'Quit Scaling', 'Quit Scaling')
    menu_bar.Append(quit_menu, 'Quit Scaling')
    frame.Bind(wx.EVT_MENU, mservice.quit_scaling, quit_quit_scaling)

    frame.SetMenuBar(menu_bar)

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
    frame.grid.Bind(grid.EVT_GRID_CELL_CHANGED, storage.set_edited)

    frame.tabpane = wx.BoxSizer()
    frame.tabs = wx.Notebook(frame.panelBottom)
    tab1 = concepts.Concepts(frame.tabs)
    tab2 = implications.Implications(frame.tabs)
    tab3 = rules.Rules(frame.tabs)
    frame.tabs.AddPage(tab1, "Concepts")
    frame.tabs.AddPage(tab2, "Implications")
    frame.tabs.AddPage(tab3, "Rules")

    frame.grid.Bind(grid.EVT_GRID_LABEL_RIGHT_CLICK, mservice.label_menu)
    frame.grid.Bind(grid.EVT_GRID_CELL_RIGHT_CLICK, mservice.cell_menu)
    frame.panelLeft.Bind(wx.EVT_RIGHT_UP, mservice.graph_menu)

    frame.csvbox.Add(frame.grid, wx.ID_ANY, wx.EXPAND)
    frame.panelTop.SetSizer(frame.csvbox)

    frame.tabpane.Add(frame.tabs, wx.ID_ANY, wx.EXPAND)
    frame.panelBottom.SetSizer(frame.tabpane)


app = wx.App()
frame = wx.Frame(None, title='FCA', size=(1200, 750))
frame.Center()
storage = datastorage.DataStorage()
tservice = tableservice.TableService(frame, storage)
gservice = graphservice.GraphService(frame, storage)
mservice = menuservice.MenuService(frame, storage, tservice, gservice)
build_ui()
frame.Show()
frame.Bind(wx.EVT_SIZE, mservice.redraw)
frame.Bind(wx.EVT_MOVE_END, mservice.redraw)
frame.Bind(wx.EVT_CLOSE, mservice.quit_scaling)
app.MainLoop()