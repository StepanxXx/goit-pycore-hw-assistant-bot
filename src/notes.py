"""Utility classes for managing notes with text content and searchable tags."""

from collections import UserList


class Tags(UserList[str]):
    """Normalized collection of unique tags for a note."""

    def add(self, tag: str):
        """Add tag if it is not already present (case-insensitive)."""
        if tag.lower() in self.data:
            return
        self.data.append(tag.lower())

    def delete(self, tag: str):
        """Remove tag if it exists."""
        for index, value in enumerate(self.data):
            if tag.lower() == value:
                self.data.pop(index)
                break

    def __str__(self):
        """Return comma-separated string of sorted tags."""
        return ", ".join(sorted(self.data))


class Note:
    """Message-like entity that stores note text and its tags."""

    def __init__(self, value: str):
        self.__value = None
        self.value = value
        self.tags = Tags()

    @property
    def value(self):
        """Return note text."""
        return self.__value

    @value.setter
    def value(self, value: str):
        """Set note text ensuring it is not empty."""
        if not value.strip():
            raise ValueError("Note text is empty")
        self.__value = value


class Notes(UserList[Note]):
    """Collection of notes supporting CRUD operations and tag lookups."""

    def add(self, note: str):
        """Create a Note from provided text and append it to the list."""
        self.data.append(Note(note))

    def show(self):
        """Return all stored notes."""
        return [
            [idx + 1, str(note.tags), note.value]
            for idx, note in enumerate(self.data)
        ]

    def edit(self, index: int, new_note: str):
        """Replace text of the note located at the provided index."""
        self.data[index].value = new_note

    def delete(self, index: int):
        """Remove a note by index."""
        self.data.pop(index)

    def find(self, query: str):
        """Return notes containing the query substring (case-insensitive)."""
        if not query:
            return []
        return [
            [idx + 1, str(note.tags), note.value]
            for idx, note in enumerate(self.data)
            if query.lower() in note.value.lower()
        ]

    def add_tag(self, index: int, tag: str):
        """Attach a tag to the note at the given index."""
        self.data[index].tags.add(tag)

    def delete_tag(self, index: int, tag: str):
        """Remove a tag from the note at the given index."""
        self.data[index].tags.delete(tag)

    def find_by_tag(self, tag: str):
        """Return notes that contain the provided tag."""
        if not tag:
            return []
        return [
            [idx + 1, str(note.tags), note.value]
            for idx, note in enumerate(self.data)
            if tag.lower() in note.tags
        ]

    def sort_by_tag(self, reverse: bool = False):
        """Return notes sorted by their tags string representation."""
        return sorted(
            [
                [idx + 1, str(note.tags), note.value]
                for idx, note in enumerate(self.data)
            ],
            key=lambda note: note[1],
            reverse=reverse,
        )
