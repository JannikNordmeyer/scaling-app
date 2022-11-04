import wx

from scaling_app import tableservice, api


class Implications(wx.Panel):
    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.frame = frame

        self.compute_button = wx.Button(self, -1, "Compute", size=wx.Size(100, 1))
        self.compute_button.Bind(wx.EVT_BUTTON, self.compute)
        self.status_text = wx.StaticText(self, -1, "Implication not yet computed.", (20, 20))

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.compute_button, 1, wx.TOP | wx.LEFT)
        self.sizer.Add(self.status_text, 8, wx.TOP | wx.LEFT)

        self.SetSizer(self.sizer)

    def compute(self, evt=None):
        objects, attributes, incidence = tableservice.get_grid_data(self.frame.result_grid)
        implications = api.request_implications(objects, attributes, incidence)

        impl_str = ""
        for i in implications["implications"]["result"]:
            impl_str += str(i[0]) + "->" + str(i[1]) + "\n"

        self.status_text.SetLabel(impl_str)

