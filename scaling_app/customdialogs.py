import wx


class CounterExampleDialog(wx.Dialog):
    def __init__(self, parent, id, title, implications, attributes, size=wx.Size(500, 10000), pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER, name='dialog'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        self.implications = implications
        self.confirmed_attributes = attributes

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.name_text = wx.StaticText(self, label="Enter the name of the new object:")
        self.name_text_entry = wx.TextCtrl(self, -1, "", size=(300, -1))
        self.attribute_text = wx.StaticText(self, label="Enter all attributes of the new object:")
        self.error_text = wx.StaticText(self, label="Error:")
        self.error_text.SetForegroundColour((255, 0, 0))
        self.attribute_text_entry = wx.TextCtrl(self, -1, "", size=(300, -1))
        self.attribute_text_entry.Bind(wx.EVT_TEXT, self.AttributesEntered)

        self.sizer.Add(self.name_text, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.sizer.Add(self.name_text_entry, 0, wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.attribute_text, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.sizer.Add(self.error_text, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.sizer.Add(self.attribute_text_entry, 0, wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, 5)

        self.line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        self.sizer.Add(self.line, 0, wx.EXPAND | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()

        self.ok_button = wx.Button(self, wx.ID_OK)
        self.ok_button.SetDefault()
        btnsizer.AddButton(self.ok_button)

        self.cancel_button = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(self.cancel_button)
        btnsizer.Realize()

        self.sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

        self.Center()
        self.error_text.Hide()
        self.Layout()

    def SetRequiredAttributes(self, implication):
        # Enters the attributes required to contradict the implication into the respective TextCtrl.
        premise = implication[0]['premise']
        default_value = ""
        for a in premise:
            default_value += a
            default_value += ", "
        self.attribute_text_entry.write(default_value)

    def GetValues(self):
        # Returns the name and attributes entered by the user.
        name = self.name_text_entry.GetLineText(0)
        attributes = []
        attributes_string = self.attribute_text_entry.GetLineText(0)
        for a in attributes_string.split(','):
            if not (str.isspace(a) or a == ""):
                attributes.append(a.lstrip().rstrip())
        return [name, attributes]

    def DisplayError(self, message):
        # Displays the error text with specified message and disables the ok button.
        self.error_text.SetLabel(message)
        self.error_text.Show()
        self.ok_button.Disable()
        self.Layout()


    def AttributesEntered(self, evt=None):
        # Checks whether any errors are present in the entered attributes and displays corresponding error text.

        if self.attribute_text_entry.GetLineText(0) == "":
            self.DisplayError("You need to at least enter one attribute.")
        else:
            name, attributes = self.GetValues()
            if set(attributes).difference(set(self.confirmed_attributes)) != set():
                self.DisplayError("Your entry contains unknown attributes.")
            else:
                self.error_text.Hide()
                self.ok_button.Enable()
                self.Layout()


