import wx

from scaling_app import tableservice, api, menuservice


class Rules(wx.Panel):
    def __init__(self, parent, frame, mservice):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.frame = frame
        self.mservice = mservice

        self.compute_button = wx.Button(self, -1, "Compute", size=wx.Size(100, 25))
        self.compute_button.Bind(wx.EVT_BUTTON, self.compute)
        self.supp_label = wx.StaticText(self, -1, "  Minimum Support:   ", (20, 20))
        self.supp_selector = wx.TextCtrl(self, value="0.5", size=wx.Size(1, 25))
        self.conf_label = wx.StaticText(self, -1, "  Minimum Confidence:   ", (20, 20))
        self.conf_selector = wx.TextCtrl(self, value="0.5", size=wx.Size(1, 25))

        self.top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.top_sizer.Add(self.compute_button, 1, wx.TOP | wx.LEFT)
        self.top_sizer.Add(self.supp_label, 1, wx.TOP | wx.LEFT)
        self.top_sizer.Add(self.supp_selector, 1, wx.TOP | wx.LEFT)
        self.top_sizer.Add(self.conf_label, 1, wx.TOP | wx.LEFT)
        self.top_sizer.Add(self.conf_selector, 1, wx.TOP | wx.LEFT)

        self.status_text = wx.StaticText(self, -1, "Rules not yet computed.", (20, 20))
        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(0, "Premise", width=750)
        self.list.InsertColumn(1, "Conclusion", width=750)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.top_sizer, 1, wx.TOP | wx.LEFT)
        self.sizer.Add(self.status_text, 1, wx.LEFT)
        self.sizer.Add(self.list, 8, wx.TOP | wx.LEFT)

        self.SetSizer(self.sizer)

    def compute(self, evt=None):
        objects, attributes, incidence = tableservice.get_grid_data(self.frame.result_grid)

        try:
            supp = float(self.supp_selector.GetLineText(0))
            conf = float(self.conf_selector.GetLineText(0))
        except:
            return

        wx.BeginBusyCursor()
        rules = api.request_rules(self.mservice.api_address, objects, attributes, incidence, supp, conf)

        if rules is None:
            menuservice.connection_error_dialog()
            wx.EndBusyCursor()
            return

        self.list.ClearAll()
        self.list.InsertColumn(0, "Premise", width=750)
        self.list.InsertColumn(1, "Conclusion", width=750)

        row_counter = 0
        for i in rules["rules"]["result"]:
            self.list.InsertItem(row_counter, str(i[0]))
            self.list.SetItem(row_counter, 1, "->  " + str(i[1]))
            row_counter += 1

        self.status_text.SetLabel("Association Rules:")
        wx.EndBusyCursor()

