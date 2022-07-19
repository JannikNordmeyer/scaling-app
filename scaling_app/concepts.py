import wx

class Concepts(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        t = wx.StaticText(self, -1, "Concepts not yet computed.", (20,20))