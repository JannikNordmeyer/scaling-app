import wx

from scaling_app import tableservice, api, menuservice


class Concepts(wx.Panel):
    def __init__(self, parent, frame, mservice):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.frame = frame
        self.mservice = mservice

        self.compute_button = wx.Button(self, -1, "Compute", size=wx.Size(100, 25))
        self.compute_button.Bind(wx.EVT_BUTTON, self.compute)
        self.status_text = wx.StaticText(self, -1, "Concepts not yet computed.", (50, 50))
        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT, size=wx.Size(2000, 550))

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.compute_button, 0, wx.TOP | wx.LEFT)
        self.sizer.Add(self.status_text, 0, wx.LEFT)
        self.sizer.Add(self.list, 0, wx.TOP | wx.LEFT)

        self.SetSizer(self.sizer)

    def compute(self, evt=None):
        # Computes concepts via API and displays them
        wx.BeginBusyCursor()

        if self.frame.top_tabs.GetSelection() == 0:
            grid = self.frame.single_valued_grid
        else:
            grid = self.frame.result_grid

        objects, attributes, incidence = tableservice.get_grid_data(grid)
        implications = api.request_concepts(self.mservice.api_address, objects, attributes, incidence)

        if implications is None:
            menuservice.connection_error_dialog()
            wx.EndBusyCursor()
            return

        self.list.ClearAll()
        self.list.InsertColumn(0, "", width=1500)

        row_counter = 0
        for i in implications["concepts"]["result"]:

            self.list.InsertItem(row_counter, str(i[0])+ " : " + str(i[1]))
            row_counter += 1

        self.status_text.SetLabel("Concepts:")
        wx.EndBusyCursor()
