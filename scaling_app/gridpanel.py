import wx
import wx.grid as grid


class GridPanel(wx.Panel):
    def __init__(self, parent, datastorage, menuservice, tableservice):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.storage = datastorage
        self.mservice = menuservice
        self.tservice = tableservice

        self.grid = grid.Grid(self.parent)
        self.grid.CreateGrid(16, 8)
        self.grid.EnableDragCell()
        self.grid.EnableDragColMove()
        self.grid.Bind(grid.EVT_GRID_CELL_CHANGED, self.storage.set_edited)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)

        self.grid.Bind(grid.EVT_GRID_LABEL_RIGHT_CLICK, self.mservice.label_menu)
        self.grid.Bind(grid.EVT_GRID_CELL_RIGHT_CLICK, self.mservice.cell_menu)

        self.grid.Bind(grid.EVT_GRID_CELL_LEFT_CLICK, self.tservice.check_toggle)
