import wx

from scaling_app import tableservice, api, menuservice


class Implications(wx.Panel):
    def __init__(self, parent, frame, mservice):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.frame = frame
        self.mservice = mservice

        self.compute_canon_button = wx.Button(self, -1, "Compute \nCanonical Base", size=wx.Size(100, 1))
        self.compute_canon_button.Bind(wx.EVT_BUTTON, self.compute_canon)
        self.compute_ganter_button = wx.Button(self, -1, "Compute \nGanter Base", size=wx.Size(100, 1))
        self.compute_ganter_button.Bind(wx.EVT_BUTTON, self.compute_canon)
        self.status_text = wx.StaticText(self, -1, "Implication not yet computed.", (20, 20))
        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(0, "Premise", width=750)
        self.list.InsertColumn(1, "Conclusion", width=750)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.compute_canon_button, 1, wx.TOP | wx.LEFT)
        self.sizer.Add(self.compute_ganter_button, 1, wx.TOP | wx.LEFT)
        self.sizer.Add(self.status_text, 1, wx.LEFT)
        self.sizer.Add(self.list, 8, wx.TOP | wx.LEFT)

        self.SetSizer(self.sizer)

    def compute_canon(self, evt=None):
        objects, attributes, incidence = tableservice.get_grid_data(self.frame.result_grid)
        implications = api.request_implications_canonical(self.mservice.api_address, objects, attributes, incidence)

        if implications is None:
            menuservice.connection_error_dialog()
            return

        self.display(implications)

    def compute_ganter(self, evt=None):
        objects, attributes, incidence = tableservice.get_grid_data(self.frame.result_grid)
        implications = api.request_implications_ganter(self.mservice.api_address, objects, attributes, incidence)

        if implications is None:
            menuservice.connection_error_dialog()
            return

        self.display(implications)

    def display(self, implications):

        self.list.ClearAll()
        self.list.InsertColumn(0, "Premise", width=750)
        self.list.InsertColumn(1, "Conclusion", width=750)

        row_counter = 0
        for i in implications["implications"]["result"]:

            self.list.InsertItem(row_counter, str(i[0]))
            self.list.SetItem(row_counter, 1, "->  " + str(i[1]))
            row_counter += 1

        self.status_text.SetLabel("Implications:")