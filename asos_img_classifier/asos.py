####2 asos.py
# object for each asos item from website

class AsosObject():
    def __init__(self, title, img, id, label, fname):
        self.title = title
        self.img = img
        self.id = id
        self.label = label
        self.fname = fname

    def get_info(self):
        return [self.title, self.id, self.fname, self.label]