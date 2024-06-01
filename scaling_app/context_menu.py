import wx
from wx import Point

from scaling_app import constants


class ContextMenu(wx.Panel):
    def __init__(self, parent, frame, mservice, tservice, scservice):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.frame = frame
        self.mservice = mservice
        self.tservice = tservice
        self.scservice = scservice

        self.button_draw = wx.Button(self, -1, "Draw Lattice", size=wx.Size(100, 25))
        self.button_draw.Bind(wx.EVT_BUTTON, self.draw)

        self.button_purge = wx.Button(self, -1, "Purge Table", size=wx.Size(100, 25))
        self.button_purge.Bind(wx.EVT_BUTTON, self.purge)

        self.button_reset = wx.Button(self, -1, "Reset Table", size=wx.Size(100, 25))
        self.button_reset.Bind(wx.EVT_BUTTON, self.reset)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.button_purge, 0, wx.TOP | wx.LEFT)
        self.sizer.Add(self.button_reset, 0, wx.TOP | wx.LEFT)
        self.sizer.Add(self.button_draw, 0, wx.TOP | wx.LEFT)

        self.SetSizer(self.sizer)

    def top_tabs_changed(self, evt):
        # called when top tabs change
        if evt.GetSelection() == 0:
            self.button_purge.Show(True)
            self.button_reset.Show(True)
            self.button_draw.Show(True)
            self.Layout()
        else:
            self.scaling_tabs_changed()

    def scaling_tabs_changed(self):
        # called when scaling tabs change
        self.button_draw.Hide()
        self.button_purge.Hide()
        self.button_reset.Hide()

        tab = self.frame.scaling_tabs.GetSelection()

        if tab > 0:
            self.button_draw.Show(True)
        if tab != 1:
            self.button_purge.Show(True)
            self.button_reset.Show(True)
        self.Layout()

    def draw(self, evt=None):
        choices = ["Dim Draw", "Freese Draw", "Standard", "Inf-Additive"]
        dialog = wx.SingleChoiceDialog(None, "Choose Layout Algorithm", "Draw Lattice",
                                       choices, wx.OK | wx.CANCEL, pos=Point(900, 400))
        answer = dialog.ShowModal()
        if answer == wx.ID_OK:
            if self.frame.top_tabs.GetSelection() == 0:
                self.scservice.get_draw_lattice(constants.dim)()
            else:
                self.tservice.get_draw_lattice(constants.dim)()
        dialog.Destroy()

    def purge(self, evt=None):
        if self.frame.top_tabs.GetSelection() == 0:
            self.scservice.purge_table()
        else:
            self.tservice.s.purge_table()

    def reset(self, evt=None):
        if self.frame.top_tabs.GetSelection() == 0:
            self.scservice.reset_table()
        else:
            self.tservice.s.reset_table()

