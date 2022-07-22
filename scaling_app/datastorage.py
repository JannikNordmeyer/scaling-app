class DataStorage:

    context = None
    data = None

    edited = False

    def set_edited(self, evt=None):
        self.edited = True

    def clear_edited(self, evt=None):
        self.edited = False
