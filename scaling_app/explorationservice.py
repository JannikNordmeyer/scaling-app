import wx

from scaling_app.api import request_exploration_step


def ask_attributes(self):
    dialog = wx.TextEntryDialog(None, "Enter Attributes:", "Attribute Exploration")
    dialog.ShowModal()
    attributes_string = dialog.GetValue()
    dialog.Destroy()
    attributes = []
    for a in attributes_string.split(","):
        attributes.append(a.lstrip().rstrip())
    return attributes

def ask_implication_holds(self, implication):
    premise = implication[0]['premise']
    conclusion = implication[0]['conclusion']
    implication_text = "Does the implication " + str(premise) + " -> " + str(conclusion) + " hold?"

    dialog = wx.MessageDialog(None, implication_text, "Attribute Exploration", wx.YES_NO)
    answer = dialog.ShowModal()
    dialog.Destroy()
    return answer

def counterexample_dialog(self, implication):
    dialog = wx.TextEntryDialog(None, "Enter the name of the new object:", "Attribute Exploration")
    dialog.ShowModal()
    name = dialog.GetValue()
    dialog.Destroy()

    dialog = wx.TextEntryDialog(None, "Enter all attributes of " + name + ":", "Attribute Exploration")
    dialog.ShowModal()
    attributes_string = dialog.GetValue()
    dialog.Destroy()
    attributes = []
    for a in attributes_string:
        attributes.append(a.lstrip().rstrip())
    return name, attributes


class ExplorationService:

    def __init__(self, frame, datastorage, menuservice):
        self.frame = frame
        self.datastorage = datastorage
        self.mservice = menuservice

    def explore(self, evt):

        objects = []
        attributes = ask_attributes(self)
        incidence = []
        implications = []

        while True:
            result = request_exploration_step(self.mservice.api_address, objects, attributes, incidence, implications)
            print(implications)
            print(result)
            implication = result['step']['result']['implications']
            if implication == []:
                print("Done")
                break
            print(implication)
            print(type(implication))

            answer = ask_implication_holds(self, implication)

            if answer == wx.ID_YES:
                implications += implication

            if answer == wx.ID_NO:
                name, incident_attributes = counterexample_dialog(self, implication)
                objects.append(name)
                for a in incident_attributes:
                    incidence.append([name, a])

