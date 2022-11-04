import wx

from scaling_app import tableservice, api


class Rules(wx.Panel):
    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.frame = frame

        self.compute_button = wx.Button(self, -1, "Compute", size=wx.Size(100, 25))
        self.compute_button.Bind(wx.EVT_BUTTON, self.compute)
        self.supp_label = wx.StaticText(self, -1, "  Minimum Support:   ", (20, 20))
        self.supp_selector = wx.TextCtrl(self, size=wx.Size(1, 25))
        self.conf_label = wx.StaticText(self, -1, "  Minimum Confidence:   ", (20, 20))
        self.conf_selector = wx.TextCtrl(self, size=wx.Size(1, 25))

        self.top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.top_sizer.Add(self.compute_button, 1, wx.TOP | wx.LEFT)
        self.top_sizer.Add(self.supp_label, 1, wx.TOP | wx.LEFT)
        self.top_sizer.Add(self.supp_selector, 1, wx.TOP | wx.LEFT)
        self.top_sizer.Add(self.conf_label, 1, wx.TOP | wx.LEFT)
        self.top_sizer.Add(self.conf_selector, 1, wx.TOP | wx.LEFT)

        self.status_text = wx.StaticText(self, -1, "Rules not yet computed.", (20, 20))

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.top_sizer, 1, wx.TOP | wx.LEFT)
        self.sizer.Add(self.status_text, 8, wx.TOP | wx.LEFT)

        self.SetSizer(self.sizer)

    def compute(self, evt=None):
        objects, attributes, incidence = tableservice.get_grid_data(self.frame.result_grid)

        try:
            supp = float(self.supp_selector.GetLineText(0))
            conf = float(self.conf_selector.GetLineText(0))
        except:
            return

        rules = api.request_rules(objects, attributes, incidence, supp, conf)
        impl_str = ""
        for i in rules["rules"]["result"]:
            impl_str += str(i[0]) + "->" + str(i[1]) + "\n"

        self.status_text.SetLabel(impl_str)
