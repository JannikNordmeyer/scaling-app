import wx
from wx import Point

from scaling_app import constants


class ContextMenu(wx.Panel):
    def __init__(self, parent, frame, mservice, tservice):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.frame = frame
        self.mservice = mservice
        self.tservice = tservice

        self.button_draw = wx.Button(self, -1, "Draw Context", size=wx.Size(100, 25))
        self.button_draw.Bind(wx.EVT_BUTTON, self.draw)
        self.button_draw.Hide()

        self.button_purge = wx.Button(self, -1, "Purge Table", size=wx.Size(100, 25))
        self.button_purge.Bind(wx.EVT_BUTTON, self.tservice.s.purge_table)

        self.button_reset = wx.Button(self, -1, "Reset Table", size=wx.Size(100, 25))
        self.button_reset.Bind(wx.EVT_BUTTON, self.tservice.s.reset_table)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.button_purge, 0, wx.TOP | wx.LEFT)
        self.sizer.Add(self.button_reset, 0, wx.TOP | wx.LEFT)
        self.sizer.Add(self.button_draw, 0, wx.TOP | wx.LEFT)

        self.SetSizer(self.sizer)
        wx.Yield()

    def page_changed(self, number):
        if number > 0:
            self.button_draw.Show(True)
        if number == 0:
            self.button_draw.Hide()
        if number == 1:
            self.button_purge.Hide()
            self.button_reset.Hide()
        if number != 1:
            self.button_purge.Show(True)
            self.button_reset.Show(True)

        self.Layout()

    def draw(self, evt=None):
        choices = ["Dim Draw", "Freese Draw", "Standard", "Inf-Additive"]
        dialog = wx.SingleChoiceDialog(None, "Choose Layout Algorithm", "Draw Context",
                                       choices, wx.OK | wx.CANCEL, pos=Point(900, 400))
        answer = dialog.ShowModal()
        if answer == wx.ID_OK:
            self.tservice.get_draw_lattice(constants.dim)()
        dialog.Destroy()
