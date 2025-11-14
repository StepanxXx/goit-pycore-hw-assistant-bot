from collections import UserList


class Notes(UserList):
    def add(self, note: str):
        self.data.append(note)

    def show(self):
        return self.data 
    
    def note_edit(self, index: int, new_note: str):
        self.data[index] = new_note
       
    def delete(self, index: int):
        self.data.pop(index)