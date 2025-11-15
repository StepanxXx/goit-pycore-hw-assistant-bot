"""Command handler class for the assistant bot."""

from tabulate import tabulate

from src.address_book import AddressBook, Record
from src.input_error import input_error


class AssistantBotHandlers:
    """Encapsulates the contact management operations."""

    def __init__(self, book: AddressBook) -> None:
        self.book = book
        self.notes: list[str] = []   # сховище нотаток

    @input_error
    def add_contact(self, args):
        """Add a new contact to the address book, checking for duplicates."""
        name, phone, *_ = args
        contact = self.book.find(name)
        message = "Contact updated."
        if contact is None:
            contact = Record(name)
            self.book.add_record(contact)
            message = "Contact added."
        if phone:
            contact.add_phone(phone)
        return message

    @input_error
    def change_contact(self, args):
        """Update the phone number for an existing contact."""
        name, old_phone, new_phone, *_ = args
        contact = self.book.find(name)
        if contact is None:
            return f'Contact "{name}" is not exists.'
        if contact.find_phone(old_phone) is None:
            return f'Phone "{old_phone}" is not exists.'
        contact.edit_phone(old_phone, new_phone)
        return "Contact updated."

    @input_error
    def show_phone(self, args):
        """Display the phone numbers for a specified contact."""
        name = args[0]
        contact = self.book.find(name)
        if contact is None:
            return f'Contact "{name}" is not exists.'
        if len(contact.phones) <= 0:
            return f'The contact "{name}" has no phones.'
        rows = [[contact.name.value, str(phone)] for phone in contact.phones]
        return tabulate(rows, headers=["Name", "Phone"], tablefmt="plain")

    @input_error
    def show_all(self):
        """Format and return a list of all contacts and their phone numbers."""
        rows = []
        for contact in self.book.data.values():
            phones = ", ".join(str(phone) for phone in contact.phones) if contact.phones else "-"
            birthday = str(contact.birthday) if contact.birthday else "-"
            rows.append([contact.name.value, phones, birthday])
        if not rows:
            return "Address book is empty."
        return tabulate(rows, headers=["Name", "Phones", "Birthday"], tablefmt="plain")

    @input_error
    def add_birthday(self, args):
        """Add the birthday for an existing contact."""
        name, birthday, *_ = args
        contact = self.book.find(name)
        if contact is None:
            return f'Contact "{name}" is not exists.'
        contact.add_birthday(birthday)
        return "Contact birthday added."

    @input_error
    def show_birthday(self, args):
        """Display the birthday for a specified contact."""
        name = args[0]
        contact = self.book.find(name)
        if contact is None:
            return f'Contact "{name}" is not exists.'
        if contact.birthday is None:
            return "Contact date of birth is not specified."
        return str(contact.birthday)

    @input_error
    def show_birthdays(self):
        """Show birthdays that will occur within the next week."""
        rows = [
            [congratulation.name, congratulation.congratulation_date]
            for congratulation in self.book.get_upcoming_birthdays()
        ]
        if not rows:
            return "No upcoming birthdays."
        return tabulate(rows, headers=["Name", "Congratulation date"], tablefmt="plain")

    @input_error
    def add_note(self, args):
        """Add a new text note."""
        note_text = " ".join(args).strip()
        if not note_text:
            raise ValueError("Note text is empty.")
        self.notes.append(note_text)
        return "Note added."

    @input_error
    def show_notes(self):
        """Show all notes as a numbered list."""
        if not self.notes:
            return "No notes available."
        rows = [[idx + 1, note] for idx, note in enumerate(self.notes)]
        return tabulate(rows, headers=["#", "Note"], tablefmt="plain")

    @input_error
    def find_note(self, args):
        """Find notes that contain the given text (case-insensitive search)."""
        query = " ".join(args).strip()
        if not query:
            raise ValueError("Search query is empty.")

        matches = [
            (idx + 1, note)
            for idx, note in enumerate(self.notes)
            if query.lower() in note.lower()
        ]

        if not matches:
            return f"No notes found for '{query}'."

        rows = [[idx, note] for idx, note in matches]
        return tabulate(rows, headers=["#", "Note"], tablefmt="plain")
