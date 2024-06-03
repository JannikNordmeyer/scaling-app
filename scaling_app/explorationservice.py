import wx
from scaling_app.api import request_exploration_step, check_connection
from scaling_app.customdialogs import NewObjectDialog, make_implication_string
from scaling_app.menuservice import connection_error_dialog
from scaling_app.tablesubservice import get_grid_data


def ask_attributes(self):
    # Displays a dialog to enter the starting attributes for the exploration.
    dialog = wx.TextEntryDialog(None, "Enter starting attributes:", "Attribute Exploration")
    dialog.ShowModal()
    attributes_string = dialog.GetValue()
    dialog.Destroy()
    attributes = []
    for a in attributes_string.split(","):
        attributes.append(a.lstrip().rstrip())
    return list(set(attributes))


def ask_starting_object(self, additional=False):
    # Displays a dialog asking if starting objects should be added
    if additional:
        question_Str = "Do you want to add another starting object?"
    else:
        question_Str = "Do you want to add starting objects?"

    dialog = wx.MessageDialog(None, question_Str, "Attribute Exploration", wx.YES_NO | wx.CANCEL)
    answer = dialog.ShowModal()
    dialog.Destroy()
    return answer


def ask_implication_holds(self, implication):
    # Displays a dialog asking whether the specified implication holds
    implication_text = "Does the following implication hold? " + "\n" + make_implication_string(implication[0])

    dialog = wx.MessageDialog(None, implication_text, "Attribute Exploration", wx.YES_NO | wx.CANCEL)
    answer = dialog.ShowModal()
    dialog.Destroy()
    return answer


def ask_object(self, implications, objects, attributes, asked_implication=None):
    # Displays a dialog for entering a new object.
    dialog = NewObjectDialog(None, wx.ID_ANY, title="Attribute Exploration", asked_implication=asked_implication, implications=implications, objects=objects, attributes=attributes)
    if asked_implication:
        dialog.SetRequiredAttributes(asked_implication)
        pass
    answer = dialog.ShowModal()
    new_object = dialog.GetValues()
    dialog.Destroy()
    if answer == wx.ID_CANCEL:
        return wx.ID_CANCEL, wx.ID_CANCEL
    else:
        return new_object

def ask_stored_implications(implications):
    # Displays a dialog asking whether the stored implications should be used for the exploration
    implication_text = "There are stored implications from the previous exploration. Do you want to use them as background knowledge?"
    for i in implications:
        implication_text += str("\n" + make_implication_string(i))

    dialog = wx.MessageDialog(None, implication_text, "Attribute Exploration", wx.YES_NO | wx.CANCEL)
    answer = dialog.ShowModal()
    dialog.Destroy()
    return answer

class ExplorationService:

    def __init__(self, frame, datastorage, menuservice, simplecontextservice, tableservice):
        self.frame = frame
        self.datastorage = datastorage
        self.mservice = menuservice
        self.scservice = simplecontextservice
        self.tservice = tableservice

        self.stored_implications = []

    def process_result(self, result, implications):
        # Displays the context resulting from the exploration step in the single valued grid and stores implications
        objects = result['step']['result']['context']['objects']
        attributes = result['step']['result']['context']['attributes']
        incidence = dict()
        for i in result['step']['result']['context']['incidence']:
            x_coord = objects.index(i[0])
            y_coord = attributes.index(i[1])
            incidence[x_coord, y_coord] = "✘"
        self.scservice.fill_context(objects, attributes, incidence)

        self.stored_implications = implications

    def explore_context(self, evt=None):
        # starts exploration algorithm with starting context
        objects, attributes, incidence = get_grid_data(self.frame.single_valued_grid)
        self.explore(objects, attributes, incidence)

    def prune_stored_implications(self, attributes):
        # removes stored implications that contain attributes not present in the exploration
        compatible_implications = []
        for i in self.stored_implications:
            implication_attributes = set(i['premise'] + i['conclusion'])
            print("Comparison:")
            print(implication_attributes)
            print(attributes)
            if implication_attributes.issubset(set(attributes)):
                compatible_implications.append(i)

        self.stored_implications = compatible_implications

    def explore(self, objects=None, attributes=None, incidence=None, evt=None):
        # Performs attribute exploration algorithm.

        wx.BeginBusyCursor()
        if not check_connection(self.mservice.api_address):
            connection_error_dialog()
            wx.EndBusyCursor()
            return
        wx.EndBusyCursor()

        # if function is called without starting context
        if incidence is None:
            objects = []
            attributes = ask_attributes(self)
            incidence = []

        implications = []

        print(attributes)
        print(self.stored_implications)
        self.prune_stored_implications(attributes)
        if self.stored_implications:
            answer = ask_stored_implications(self.stored_implications)
            if answer == wx.ID_YES:
                implications = self.stored_implications

        # Add starting objects
        answer = ask_starting_object(self)
        while answer == wx.ID_YES:

            name, incident_attributes = ask_object(self, implications, objects, attributes)
            objects.append(name)
            for a in incident_attributes:
                incidence.append([name, a])

            answer = ask_starting_object(self, True)
        if answer == wx.ID_CANCEL:
            return

        # Exploration
        while True:
            result = request_exploration_step(self.mservice.api_address, objects, attributes, incidence, implications)
            asked_implication = result['step']['result']['implications']

            self.process_result(result, implications)

            # No further implications, Exploration over:
            if not asked_implication:
                break

            answer = ask_implication_holds(self, asked_implication)

            if answer == wx.ID_CANCEL:
                self.process_result(result, implications)
                break

            if answer == wx.ID_YES:
                implications += asked_implication

            if answer == wx.ID_NO:
                name, incident_attributes = ask_object(self, implications, objects, attributes, asked_implication)

                if name == wx.ID_CANCEL:
                    self.process_result(result, implications)
                    break

                objects.append(name)
                for a in incident_attributes:
                    incidence.append([name, a])
