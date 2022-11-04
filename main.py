import wx
import wx.grid as grid
from scaling_app import menuservice, tableservice, graphservice, datastorage, graphpanel, statservice
from scaling_app import concepts
from scaling_app import implications
from scaling_app import rules
import gettext
import locale


def build_ui():

    """if locale.getlocale()[0] == 'de_DE':

        lang = gettext.translation('messages', localedir='locale', languages=[locale.getlocale()[0]])
        lang.install()

        _ = lang.gettext
    else:
        _ = gettext.gettext"""
    _ = gettext.gettext

    # Top Menus
    menu_bar = wx.MenuBar()

    file_menu = wx.Menu()
    file_load = file_menu.Append(wx.ID_ANY, _('Load Data'), _('Load Data'))
    graph_load = file_menu.Append(wx.ID_ANY, _('Load Lattice'), _('Load Lattice'))
    file_save = file_menu.Append(wx.ID_ANY, _('Save Data'), _('Save Data'))
    file_menu.AppendSeparator()
    file_quit = file_menu.Append(wx.ID_ANY, _('Empty Frame'), _('Empty Frame'))
    menu_bar.Append(file_menu, _('Data'))
    frame.Bind(wx.EVT_MENU, mservice.load_data, file_load)
    frame.Bind(wx.EVT_MENU, mservice.load_lattice, graph_load)
    frame.Bind(wx.EVT_MENU, mservice.save_data, file_save)
    frame.Bind(wx.EVT_MENU, mservice.empty_frame, file_quit)

    help_menu = wx.Menu()
    help_about = help_menu.Append(wx.ID_ANY, _('About'), _('About'))
    help_manual = help_menu.Append(wx.ID_ANY, _('Manual'), _('Manual'))
    menu_bar.Append(help_menu, _('Help'))
    frame.Bind(wx.EVT_MENU, mservice.about, help_about)
    frame.Bind(wx.EVT_MENU, mservice.manual, help_manual)

    comp_menu = wx.Menu()
    comp_concepts = comp_menu.Append(wx.ID_ANY, _('Compute Concepts'), _('Compute Concepts'))
    comp_implications = comp_menu.Append(wx.ID_ANY, _('Compute Implications'), _('Compute Implications'))
    comp_rules = comp_menu.Append(wx.ID_ANY, _('Compute Rules'), _('Compute Rules'))
    menu_bar.Append(comp_menu, _('Compute'))

    connect_menu = wx.Menu()
    connect = connect_menu.Append(wx.ID_ANY, _('Connect to API'), _('Connect to API'))
    frame.Bind(wx.EVT_MENU, mservice.connect, connect)
    menu_bar.Append(connect_menu, _('Connect to API'))

    quit_menu = wx.Menu()
    quit_quit_scaling = quit_menu.Append(wx.ID_EXIT, _('Quit Scaling'), _('Quit Scaling'))
    menu_bar.Append(quit_menu, _('Quit Scaling'))
    frame.Bind(wx.EVT_MENU, mservice.quit_scaling, quit_quit_scaling)

    frame.SetMenuBar(menu_bar)

    # Screen Layout
    frame.hsplitter = wx.SplitterWindow(frame, style=wx.SP_LIVE_UPDATE)
    frame.vsplitter = wx.SplitterWindow(frame.hsplitter, style=wx.SP_LIVE_UPDATE)

    frame.panelLeft = wx.Panel(frame.hsplitter, wx.ID_ANY, style=wx.BORDER_SUNKEN)
    frame.panelTop = wx.Panel(frame.vsplitter, wx.ID_ANY, style=wx.BORDER_SUNKEN)
    frame.panelBottom = wx.Panel(frame.vsplitter, wx.ID_ANY, style=wx.BORDER_SUNKEN)

    frame.vsplitter.SplitHorizontally(frame.panelTop, frame.panelBottom)
    frame.hsplitter.SplitVertically(frame.panelLeft, frame.vsplitter)
    frame.hsplitter.SetMinimumPaneSize(100)
    frame.hsplitter.SetSashPosition(400)
    frame.vsplitter.SetMinimumPaneSize(100)
    frame.vsplitter.SetSashPosition(400)

    # Table Headers
    frame.csvbox = wx.BoxSizer(wx.VERTICAL)
    frame.csvtabs = wx.Notebook(frame.panelTop)
    frame.main_grid = grid.Grid(frame.csvtabs)
    frame.main_grid.CreateGrid(16, 8)
    frame.main_grid.EnableDragCell()
    frame.main_grid.EnableDragColMove()
    frame.main_grid.Bind(grid.EVT_GRID_CELL_CHANGED, tservice.cell_changed)
    frame.main_grid.Bind(grid.EVT_GRID_LABEL_RIGHT_CLICK, mservice.label_menu)
    frame.main_grid.Bind(grid.EVT_GRID_CELL_RIGHT_CLICK, mservice.cell_menu)

    frame.sizer = wx.BoxSizer(wx.HORIZONTAL)
    frame.sizer.Add(frame.main_grid, 1, wx.EXPAND | wx.ALL, 5)

    frame.main_grid.Bind(grid.EVT_GRID_CELL_LEFT_CLICK, tservice.check_toggle)
    frame.csvtabs.AddPage(frame.main_grid, _("Dataset"))
    storage.tabs.append(frame.main_grid)
    tservice.current_grid = frame.main_grid

    frame.result_grid = grid.Grid(frame.csvtabs)
    frame.result_grid.CreateGrid(16, 8)
    frame.result_grid.EnableEditing(False)
    frame.result_grid.Bind(grid.EVT_GRID_CELL_RIGHT_CLICK, mservice.cell_menu)

    frame.csvtabs.AddPage(frame.result_grid, _("Scaled Context"))
    storage.tabs.append(frame.result_grid)

    frame.csvtabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, tservice.get_save_to_storage())

    # Bottom Tabs
    frame.tabpane = wx.BoxSizer()
    frame.tabs = wx.Notebook(frame.panelBottom)
    concepts_tab = concepts.Concepts(frame.tabs)
    implications_tab = implications.Implications(frame.tabs, frame, mservice)
    rules_tab = rules.Rules(frame.tabs, frame, mservice)

    frame.Bind(wx.EVT_MENU, mservice.comp_concepts, comp_concepts)
    frame.Bind(wx.EVT_MENU, implications_tab.compute, comp_implications)
    frame.Bind(wx.EVT_MENU, rules_tab.compute, comp_rules)

    frame.tabs.AddPage(concepts_tab, _("Concepts"))
    frame.tabs.AddPage(implications_tab, _("Implications"))
    frame.tabs.AddPage(rules_tab, _("Rules"))

    frame.csvbox.Add(frame.csvtabs, wx.ID_ANY, wx.EXPAND)
    frame.panelTop.SetSizer(frame.csvbox)

    frame.tabpane.Add(frame.tabs, wx.ID_ANY, wx.EXPAND)
    frame.panelBottom.SetSizer(frame.tabpane)

    # Graph Box
    frame.graphbox = wx.BoxSizer(wx.VERTICAL)
    frame.graph = graphpanel.GraphPanel(frame.panelLeft, mservice, storage)

    frame.graphbox.Add(frame.graph, wx.ID_ANY, wx.EXPAND)
    frame.panelLeft.SetSizer(frame.graphbox)


app = wx.App()
frame = wx.Frame(None, title='FCA', size=(1200, 750))
frame.Center()
storage = datastorage.DataStorage()
tservice = tableservice.TableService(frame, storage)
gservice = graphservice.GraphService(frame, storage)
sservice = statservice.Statservice(frame, tservice, storage)
mservice = menuservice.MenuService(frame, storage, tservice, gservice, sservice)
sservice.menuservice = mservice
tservice.mservice = mservice
tservice.sservice = sservice
tservice.gservice = gservice
build_ui()
frame.Show()
frame.Bind(wx.EVT_CLOSE, mservice.quit_scaling)
app.MainLoop()
