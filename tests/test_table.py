import unittest
import wx
from scaling_app.main import build_ui
from scaling_app import menuservice
import wx.grid as grid

#nonfunctional test
class TableTest(unittest.TestCase):

    def test_getDeleteRow(self):

        #frame = wx.Frame(None, title='FCA', size=(1200, 750))
        #buildUI(frame)
        #service = menuservice.menuService(frame)
        #labelEvent = grid.GridEvent(row=3)
        #service.getDeleteRow(labelEvent)

        self.assertEqual(True, False)  # add assertion here

