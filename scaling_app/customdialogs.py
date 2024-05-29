import wx


def make_implication_string(implication):
    # Returs a string representing the specified implication for use in dialogs
    premise_string = str(implication['premise']).replace("[", "").replace("]", "").replace("'", "")
    if premise_string == "":
        premise_string = "∅"

    conclusion_string = str(implication['conclusion']).replace("[", "").replace("]", "").replace("'", "")

    implication_string = premise_string + "-> " + conclusion_string
    return implication_string


class NewObjectDialog(wx.Dialog):
    def __init__(self, parent, id, title, asked_implication, implications, objects, attributes, size=wx.Size(500, 10000), pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='dialog'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        self.asked_implication = asked_implication
        self.implications = implications
        self.objects = objects
        self.attributes = attributes

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.name_text = wx.StaticText(self, label="Enter the name of the new object:")
        self.name_error_text = wx.StaticText(self, label="Error:")
        self.name_error_text.SetForegroundColour((255, 0, 0))
        self.name_text_entry = wx.TextCtrl(self, -1, "", size=(300, -1))
        self.name_text_entry.Bind(wx.EVT_TEXT, self.NameEntered)
        self.attribute_text = wx.StaticText(self, label="Enter all attributes of the new object:")
        self.attribute_error_text = wx.StaticText(self, label="Error:")
        self.attribute_error_text.SetForegroundColour((255, 0, 0))

        self.attribute_selector = wx.ScrolledWindow(self, size=(300, 100))
        self.attribute_selector.SetScrollbars(1, 10, 1, 10)
        self.attribute_checkbox_dict = dict()
        self.attribute_sizer = self.generate_attribute_sizer()
        self.attribute_selector.SetSizer(self.attribute_sizer)

        self.sizer.Add(self.name_text, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.sizer.Add(self.name_error_text, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.sizer.Add(self.name_text_entry, 0, wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.attribute_text, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.sizer.Add(self.attribute_error_text, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.sizer.Add(self.attribute_selector, 0, wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, 5)

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
        self.name_error_text.Hide()
        self.attribute_error_text.Hide()
        self.NameEntered()
        self.Layout()

    def generate_attribute_sizer(self):
        # Generates a boxsizer containing checkboxes for each attribute
        attribute_sizer = wx.BoxSizer(wx.VERTICAL)

        for a in self.attributes:
            checkbox = wx.CheckBox(self.attribute_selector, label=a)
            checkbox.Bind(wx.EVT_CHECKBOX, self.AttributesEntered)
            self.attribute_checkbox_dict[a] = checkbox
            attribute_sizer.Add(checkbox)
        return attribute_sizer

    def SetRequiredAttributes(self, asked_implication):
        # Checks the checkboxes for each attribute required to contradict the implication.
        premise = asked_implication[0]['premise']
        for a in premise:
            self.attribute_checkbox_dict[a].SetValue(True)
            self.attribute_checkbox_dict[a].Disable()

    def GetValues(self):
        # Returns the name and attributes entered by the user.
        name = self.name_text_entry.GetLineText(0).lstrip().rstrip()
        attributes = []
        for attribute, checkbox in self.attribute_checkbox_dict.items():
            if checkbox.GetValue():
                attributes.append(attribute)
        return [name, attributes]

    def DisplayNameError(self, message):
        # Displays the error text with specified message and disables the ok button.
        self.name_error_text.SetLabel(message)
        self.name_error_text.Show()
        self.ok_button.Disable()
        self.Fit()
        self.Layout()

    def DisplayAttributeError(self, message):
        # Displays the error text with specified message and disables the ok button.
        self.attribute_error_text.SetLabel(message)
        self.attribute_error_text.Show()
        self.ok_button.Disable()
        self.Fit()
        self.Layout()

    def ClearNameError(self):
        # Removes displayed error message.
        self.name_error_text.Hide()
        self.ok_button.Enable()
        self.Fit()
        self.Layout()

    def ClearAttributeError(self):
        # Removes displayed error message.
        self.attribute_error_text.Hide()
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

    def NameEntered(self, evt=None):
        # Checks whether any errors are present in the entered object name and displays corresponding error text.
        name, attributes = self.GetValues()
        if name == "":
            self.DisplayNameError("Object name must not be empty.")
        elif name in self.objects:
            self.DisplayNameError("A object with this name already exists.")
        else:
            self.ClearNameError()

    def AttributesEntered(self, evt=None):
        # Checks whether any errors are present in the entered attributes and displays corresponding error text.
        name, attributes = self.GetValues()
        contradicted_impl = self.ContradictsKnownImplication()
        if set(attributes).difference(set(self.attributes)) != set():
            self.DisplayAttributeError("Your entry contains unknown attributes.")
        elif self.NoContradiction():
            self.DisplayAttributeError("Your entry does not contradict the implication\n " + make_implication_string(self.asked_implication[0]) + ".")
        elif contradicted_impl:
            self.DisplayAttributeError("Your entry contradicts the previously confirmed implication\n " + make_implication_string(contradicted_impl) + ".")
        else:
            self.ClearAttributeError()


