import wx


class NewObjectDialog(wx.Dialog):
    def __init__(self, parent, id, title, asked_implication, implications, attributes, size=wx.Size(500, 10000), pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER, name='dialog'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        self.asked_implication = asked_implication
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

    def SetRequiredAttributes(self, asked_implication):
        # Enters the attributes required to contradict the implication into the respective TextCtrl.
        premise = asked_implication[0]['premise']
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
        self.Fit()
        self.Layout()

    def ClearError(self):
        # Removes displayed error message.
        self.error_text.Hide()
        self.ok_button.Enable()
        self.Fit()
        self.Layout()

    def NoContradiction(self):
        # Computes whether the currently entered set of attributes contradicts the asked implication.
        # Always returns False, if asked implication is None
        if self.asked_implication is None:
            return False
        name, attributes = self.GetValues()
        premise = self.asked_implication[0]['premise']
        conclusion = self.asked_implication[0]['conclusion']
        if not set(premise).issubset(attributes) or (set(premise).issubset(attributes) and set(conclusion).issubset(attributes)):
            return True
        else:
            return False

    def ContradictsKnownImplication(self):
        # Computes whether the currently entered set of attributes contradicts a previously confirmed implication.
        # Returns the contradicted implication if it exists.
        name, attributes = self.GetValues()
        for i in self.implications:
            premise = i['premise']
            conclusion = i['conclusion']
            if set(premise).issubset(attributes) and not set(conclusion).issubset(attributes):
                return i
        return False


    def AttributesEntered(self, evt=None):
        # Checks whether any errors are present in the entered attributes and displays corresponding error text.
        name, attributes = self.GetValues()
        contradicted_impl = self.ContradictsKnownImplication()
        if set(attributes).difference(set(self.confirmed_attributes)) != set():
            self.DisplayError("Your entry contains unknown attributes.")
        elif self.NoContradiction():
            self.DisplayError("Your entry does not contradict the implication\n " + str(self.asked_implication[0]['premise']) + " -> " + str(self.asked_implication[0]['conclusion']) + ".")
        elif contradicted_impl:
            self.DisplayError("Your entry contradicts the previously confirmed implication\n " + str(contradicted_impl['premise']) + " -> " + str(contradicted_impl['conclusion']) + ".")
        else:
            self.ClearError()


