class Archive:
    title = ""
    body = ""
    def __init__(self, title = "", body = ""):
        self.title = title
        self.body = body

class Archives:
    archive_list = []
    def __init__(self, empty = True):
        if empty:
            self.archive_list = []
        else:
            for i in range(5):
                self.archive_list.append(Archive(title="archive " + str(i+1), body="Test"))
                for j in range((i+1)*50):
                    self.archive_list[i].body = self.archive_list[i].body + "TEST"

    def print_list(self):
        for element in self.archive_list:
            print(element.title)
