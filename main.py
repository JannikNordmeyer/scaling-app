import wx
import wx.grid as grid
from scaling_app import menuservice, tableservice, graphservice, datastorage, graphpanel, statservice, \
    explorationservice, simplecontextservice
from scaling_app import concepts
from scaling_app import implications
from scaling_app import rules
import gettext
import locale
from scaling_app.context_menu import ContextMenu

def build_ui():
    # Builds overall layout of the app

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
    fca_load = file_menu.Append(wx.ID_ANY, _('Load FCA'), _('Load FCA'))
    file_save = file_menu.Append(wx.ID_ANY, _('Save Data'), _('Save Data'))
    save_json = file_menu.Append(wx.ID_ANY, _('Save to JSON'), _('Save to JSON'))
    file_menu.AppendSeparator()
    file_quit = file_menu.Append(wx.ID_ANY, _('Empty Frame'), _('Empty Frame'))
    menu_bar.Append(file_menu, _('Data'))
    frame.Bind(wx.EVT_MENU, mservice.load_data, file_load)
    frame.Bind(wx.EVT_MENU, mservice.load_lattice, graph_load)
    frame.Bind(wx.EVT_MENU, mservice.load_fca, fca_load)
    frame.Bind(wx.EVT_MENU, mservice.save_data, file_save)
    frame.Bind(wx.EVT_MENU, mservice.save_json, save_json)
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

    explore_menu = wx.Menu()
    explore_attributes = explore_menu.Append(wx.ID_ANY, _('Explore Attributes'), _('Explore Attributes'))
    frame.Bind(wx.EVT_MENU, eservice.explore, explore_attributes)
    menu_bar.Append(explore_menu, _('Explore Attributes'))

    quit_menu = wx.Menu()
    quit_quit_scaling = quit_menu.Append(wx.ID_EXIT, _('Quit Scaling'), _('Quit Scaling'))
    menu_bar.Append(quit_menu, _('Quit Scaling'))
    frame.Bind(wx.EVT_MENU, mservice.quit_scaling, quit_quit_scaling)

    frame.SetMenuBar(menu_bar)

    # Screen Layout
    frame.hsplitter = wx.SplitterWindow(frame, style=wx.SP_LIVE_UPDATE)
    frame.vsplitter = wx.SplitterWindow(frame.hsplitter, style=wx.SP_LIVE_UPDATE)
    frame.gridsplitter = wx.SplitterWindow(frame.vsplitter, style=wx.SP_LIVE_UPDATE)

    frame.panelLeft = wx.Panel(frame.hsplitter, wx.ID_ANY, style=wx.BORDER_SUNKEN)
    frame.panelTop = wx.Panel(frame.gridsplitter, wx.ID_ANY, style=wx.BORDER_SUNKEN)
    frame.panelBottom = wx.Panel(frame.vsplitter, wx.ID_ANY, style=wx.BORDER_SUNKEN)
    frame.menupanel = ContextMenu(frame.gridsplitter, frame, mservice, tservice, scservice)

    frame.gridsplitter.SplitVertically(frame.panelTop, frame.menupanel)
    frame.gridsplitter.SetMinimumPaneSize(100)
    frame.gridsplitter.SetSashPosition(2000)
    frame.vsplitter.SplitHorizontally(frame.gridsplitter, frame.panelBottom)
    frame.vsplitter.SetMinimumPaneSize(100)
    frame.vsplitter.SetSashPosition(400)
    frame.hsplitter.SplitVertically(frame.panelLeft, frame.vsplitter)
    frame.hsplitter.SetMinimumPaneSize(100)
    frame.hsplitter.SetSashPosition(400)


    # Top Tabs
    frame.top_tab_sizer = wx.BoxSizer()
    frame.top_tabs = wx.Notebook(frame.panelTop)
    frame.top_tabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, frame.menupanel.top_tabs_changed)

    frame.formal_context_panel = wx.Panel(frame.top_tabs)
    frame.scaling_panel = wx.Panel(frame.top_tabs)

    # Simple Context
    frame.formal_context_box = wx.BoxSizer(wx.VERTICAL)
    frame.single_valued_grid = grid.Grid(frame.formal_context_panel)
    frame.single_valued_grid.CreateGrid(16, 8)
    frame.single_valued_grid.EnableDragCell()
    frame.single_valued_grid.EnableDragColMove()
    frame.single_valued_grid.Bind(grid.EVT_GRID_LABEL_RIGHT_CLICK, mservice.simple_label_menu)
    frame.single_valued_grid.Bind(grid.EVT_GRID_CELL_RIGHT_CLICK, mservice.simple_cell_menu)
    frame.single_valued_grid.Bind(grid.EVT_GRID_CELL_LEFT_CLICK, scservice.toggle_cell)

    frame.formal_context_box.Add(frame.single_valued_grid, 1, wx.EXPAND | wx.ALL, 5)
    frame.formal_context_panel.SetSizer(frame.formal_context_box)

    # Scale Many Valued Context
    frame.scaling_box = wx.BoxSizer(wx.VERTICAL)
    frame.scaling_tabs = wx.Notebook(frame.scaling_panel)
    frame.many_valued_grid = grid.Grid(frame.scaling_tabs)
    frame.many_valued_grid.CreateGrid(16, 8)
    frame.many_valued_grid.EnableDragCell()
    frame.many_valued_grid.EnableDragColMove()
    frame.many_valued_grid.Bind(grid.EVT_GRID_CELL_CHANGED, tservice.cell_changed)
    frame.many_valued_grid.Bind(grid.EVT_GRID_LABEL_RIGHT_CLICK, mservice.scaling_label_menu)
    frame.many_valued_grid.Bind(grid.EVT_GRID_CELL_RIGHT_CLICK, mservice.scaling_cell_menu)

    frame.many_valued_grid_sizer = wx.BoxSizer(wx.HORIZONTAL)
    frame.many_valued_grid_sizer.Add(frame.many_valued_grid, 1, wx.EXPAND | wx.ALL, 5)

    frame.many_valued_grid.Bind(grid.EVT_GRID_CELL_LEFT_CLICK, tservice.check_toggle)
    frame.scaling_tabs.AddPage(frame.many_valued_grid, _("Many Valued Context"))
    storage.grid_tabs.append(frame.many_valued_grid)
    tservice.current_grid = frame.many_valued_grid

    frame.result_grid = grid.Grid(frame.scaling_tabs)
    frame.result_grid.CreateGrid(16, 8)
    frame.result_grid.EnableEditing(False)
    frame.result_grid.Bind(grid.EVT_GRID_CELL_RIGHT_CLICK, mservice.scaling_cell_menu)

    frame.scaling_tabs.AddPage(frame.result_grid, _("Scaled Context"))
    storage.grid_tabs.append(frame.result_grid)

    frame.scaling_tabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, mservice.scaling_tab_changed)

    frame.scaling_box.Add(frame.scaling_tabs, wx.ID_ANY, wx.EXPAND)
    frame.scaling_panel.SetSizer(frame.scaling_box)


    frame.top_tabs.AddPage(frame.formal_context_panel, _("Formal Context"))
    frame.top_tabs.AddPage(frame.scaling_panel, _("Conceptual Scaling"))


    # Bottom Tabs
    frame.bottom_tab_sizer = wx.BoxSizer()
    frame.bottom_tabs = wx.Notebook(frame.panelBottom)
    concepts_tab = concepts.Concepts(frame.bottom_tabs, frame, mservice)
    implications_tab = implications.Implications(frame.bottom_tabs, frame, mservice)
    rules_tab = rules.Rules(frame.bottom_tabs, frame, mservice)

    frame.Bind(wx.EVT_MENU, concepts_tab.compute, comp_concepts)
    frame.Bind(wx.EVT_MENU, implications_tab.compute_canon, comp_implications)
    frame.Bind(wx.EVT_MENU, rules_tab.compute, comp_rules)

    frame.bottom_tabs.AddPage(concepts_tab, _("Concepts"))
    frame.bottom_tabs.AddPage(implications_tab, _("Implications"))
    frame.bottom_tabs.AddPage(rules_tab, _("Rules"))

    storage.concepts_tab = concepts_tab
    storage.implications_tab = implications_tab
    storage.rules_tab = rules_tab



    frame.bottom_tab_sizer.Add(frame.bottom_tabs, wx.ID_ANY, wx.EXPAND)
    frame.panelBottom.SetSizer(frame.bottom_tab_sizer)

    frame.top_tab_sizer.Add(frame.top_tabs, wx.ID_ANY, wx.EXPAND)
    frame.panelTop.SetSizer(frame.top_tab_sizer)
    frame.panelTop.Layout()




    # Graph Box
    frame.graphbox = wx.BoxSizer(wx.VERTICAL)
    frame.graph = graphpanel.GraphPanel(frame.panelLeft, mservice, storage)

    frame.graphbox.Add(frame.graph, wx.ID_ANY, wx.EXPAND)
    frame.panelLeft.SetSizer(frame.graphbox)

# Initialize frame and initializes and connects all service classes
app = wx.App()
frame = wx.Frame(None, title='FCA', size=(1200, 750))
frame.Center()
frame.Maximize(True)
storage = datastorage.DataStorage()
tservice = tableservice.TableService(frame, storage)
scservice = simplecontextservice.SimpleContextService(frame, storage)
gservice = graphservice.GraphService(frame, storage)
sservice = statservice.Statservice(frame, tservice, storage)
mservice = menuservice.MenuService(frame, storage, scservice, tservice, gservice, sservice)
eservice = explorationservice.ExplorationService(frame, storage, mservice, scservice, tservice)
sservice.menuservice = mservice
scservice.menuservice = mservice
scservice.graphservice = gservice
tservice.mservice = mservice
tservice.sservice = sservice
tservice.gservice = gservice
build_ui()
frame.Show()
frame.Bind(wx.EVT_CLOSE, mservice.quit_scaling)
app.MainLoop()
