from collections import UserList


class Notes(UserList):
    def add(self, note: str):
        self.data.append(note)

    def show(self):
        return self.data 