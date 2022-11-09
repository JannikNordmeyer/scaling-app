import wx

from scaling_app import tableservice, api, menuservice


class Concepts(wx.Panel):
    def __init__(self, parent, frame, mservice):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.frame = frame
        self.mservice = mservice

        self.compute_button = wx.Button(self, -1, "Compute", size=wx.Size(100, 1))
        self.compute_button.Bind(wx.EVT_BUTTON, self.compute)
        self.status_text = wx.StaticText(self, -1, "Concepts not yet computed.", (20, 20))
        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.compute_button, 1, wx.TOP | wx.LEFT)
        self.sizer.Add(self.status_text, 1, wx.LEFT)
        self.sizer.Add(self.list, 8, wx.TOP | wx.LEFT)

        self.SetSizer(self.sizer)

    def compute(self, evt=None):
        objects, attributes, incidence = tableservice.get_grid_data(self.frame.result_grid)
        implications = api.request_concepts(self.mservice.api_address, objects, attributes, incidence)

        if implications is None:
            menuservice.connection_error_dialog()
            return

        self.list.ClearAll()
        self.list.InsertColumn(0, "", width=1500)

        row_counter = 0
        for i in implications["concepts"]["result"]:

            self.list.InsertItem(row_counter, str(i[0]))
            row_counter += 1

        self.status_text.SetLabel("Concepts:")
