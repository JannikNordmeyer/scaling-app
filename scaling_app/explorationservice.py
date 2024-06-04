import wx
from wx import MessageDialog

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


def ask_starting_object(additional=False):
    # Displays a dialog asking if starting objects should be added
    if additional:
        question_Str = "Do you want to add another starting object?"
    else:
        question_Str = "Do you want to add starting objects?"

    dialog = wx.MessageDialog(None, question_Str, "Attribute Exploration", wx.YES_NO | wx.CANCEL)
    answer = dialog.ShowModal()
    dialog.Destroy()
    return answer


def ask_additional_counterexample():
    # Displays a dialog asking if the user wants to provide an additional counterexample
    dialog = wx.MessageDialog(None, "Do you want to provide an additional counterexample?", "Attribute Exploration", wx.YES_NO | wx.CANCEL)
    answer = dialog.ShowModal()
    dialog.Destroy()
    return answer


def ask_implication_holds(implication):
    # Displays a dialog asking whether the specified implication holds
    implication_text = "Does the following implication hold? " + "\n" + make_implication_string(implication[0])

    dialog = wx.MessageDialog(None, implication_text, "Attribute Exploration", wx.YES_NO | wx.CANCEL)
    answer = dialog.ShowModal()
    dialog.Destroy()
    return answer


def ask_object(implications, objects, attributes, asked_implication=None):
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


class ExplorationService:

    def __init__(self, frame, datastorage, menuservice, simplecontextservice, tableservice):
        self.frame = frame
        self.datastorage = datastorage
        self.mservice = menuservice
        self.scservice = simplecontextservice
        self.tservice = tableservice

        # saves state of the context if exploration is cancelled
        self.stored_objects = []
        self.stored_attributes = []
        self.stored_incidence = []
        self.stored_implications = []

    def clear_state(self):
        # removes stored state
        self.stored_objects = []
        self.stored_attributes = []
        self.stored_incidence = []
        self.stored_implications = []

    def process_result(self, objects, attributes, incidence, implications):
        # Displays the context resulting from the exploration step in the single valued grid and stores state
        incidence_dict = dict()
        for i in incidence:
            x_coord = objects.index(i[0])
            y_coord = attributes.index(i[1])
            incidence_dict[x_coord, y_coord] = "✘"
        self.scservice.fill_context(objects, attributes, incidence_dict)

        self.stored_objects = objects
        self.stored_attributes = attributes
        self.stored_incidence = incidence
        self.stored_implications = implications

    def explore_context(self, evt=None):
        # starts exploration algorithm with starting context
        objects, attributes, incidence = get_grid_data(self.frame.single_valued_grid)
        self.explore(objects, attributes, incidence, [])

    def continue_exploration(self, evt=None):
        if not self.stored_objects:
            dialog = MessageDialog(None, "No cancelled Exploration to continue.", "Attribute Exploration")
            dialog.ShowModal()
            dialog.Destroy()
            return
        else:
            self.explore(self.stored_objects, self.stored_attributes, self.stored_incidence, self.stored_implications)

    def explore(self, objects=None, attributes=None, incidence=None, implications=None, evt=None):
        # Performs attribute exploration algorithm.

        wx.BeginBusyCursor()
        if not check_connection(self.mservice.api_address):
            connection_error_dialog()
            wx.EndBusyCursor()
            return
        wx.EndBusyCursor()

        # if function is called without starting context or continuing from cancelled exploration
        if incidence is None:
            self.clear_state()
            objects = []
            attributes = ask_attributes(self)
            incidence = []
            implications = []
            # Add starting objects
            answer = ask_starting_object()
            while answer == wx.ID_YES:

                name, incident_attributes = ask_object(implications, objects, attributes)
                if answer == wx.ID_CANCEL:
                    return
                objects.append(name)
                for a in incident_attributes:
                    incidence.append([name, a])

                answer = ask_starting_object(True)
            if answer == wx.ID_CANCEL:
                return

        # Exploration
        while True:
            result = request_exploration_step(self.mservice.api_address, objects, attributes, incidence, implications)
            asked_implication = result['step']['result']['implications']

            self.process_result(objects, attributes, incidence, implications)

            # No further implications, Exploration over:
            if not asked_implication:
                self.clear_state()
                break

            answer = ask_implication_holds(asked_implication)

            if answer == wx.ID_CANCEL:
                self.process_result(objects, attributes, incidence, implications)
                return

            if answer == wx.ID_YES:
                implications += asked_implication

            if answer == wx.ID_NO:
                example_required = True
                while example_required:
                    name, incident_attributes = ask_object(implications, objects, attributes, asked_implication)

                    if name == wx.ID_CANCEL:
                        self.process_result(objects, attributes, incidence, implications)
                        return

                    objects.append(name)
                    for a in incident_attributes:
                        incidence.append([name, a])

                    answer = ask_additional_counterexample()
                    if answer == wx.ID_CANCEL:
                        self.process_result(objects, attributes, incidence, implications)
                        return
                    if answer == wx.ID_NO:
                        example_required = False
