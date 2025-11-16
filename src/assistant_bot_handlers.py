"""Command handler class for the assistant bot."""

from typing import List

from tabulate import tabulate

from src.notes import Notes
from src.address_book import AddressBook, Record
from src.input_error import input_error


class AssistantBotHandlers:
    """Encapsulates the contact management operations."""

    def __init__(self, book: AddressBook, notes: Notes) -> None:
        """Store shared address book and notes references."""
        self.book = book
        self.notes = notes

    @input_error
    def add_note(self, args):
        """Create a new note composed from all provided arguments."""
        note = " ".join(args)
        if not note:
            return "Note text is empty."
        self.notes.add(note)
        return "Note added."

    @input_error
    def show_notes(self):
        """Return the full notes list formatted as a readable table."""
        if self.notes:
            rows = self.notes.show()
            return tabulate(
                rows,
                headers=["№", "Tags", "Note"],
                tablefmt="plain",
            )
        return "Notes are empty."

    @input_error
    def edit_note(self, args):
        """Replace a note by its index with the provided text."""
        index, *new_note = args
        note = " ".join(new_note)
        real_index = int(index) - 1
        if not note:
            return "Note text is empty."
        if not 0 <= real_index < len(self.notes):
            return "No note found for this number."
        self.notes.edit(real_index, note)
        return "Note updated."

    @input_error
    def delete_note(self, args):
        """Remove a note by its displayed index."""
        index = int(args[0]) - 1
        if 0 <= index < len(self.notes):
            self.notes.delete(index)
        else:
            return "No note found for this number."
        return "Note deleted."

    @input_error
    def find_note(self, args):
        """Find notes that contain the given text (case-insensitive search)."""
        query = " ".join(args)
        if not query:
            return "Search query is empty."
        matches = self.notes.find(query)
        if not matches:
            return f"No notes found for '{query}'."
        return tabulate(
            matches,
            headers=["№", "Tags", "Note"],
            tablefmt="plain",
        )

    @input_error
    def add_note_tag(self, args):
        """Append a tag to the note addressed by its displayed index."""
        index, *new_tag = args
        tag = " ".join(new_tag)
        real_index = int(index) - 1
        if not tag:
            return "Tag text is empty."
        if not 0 <= real_index < len(self.notes):
            return "No note found for this number."
        self.notes.add_tag(real_index, tag)
        return "Note updated."

    @input_error
    def delete_note_tag(self, args):
        """Remove the provided tag from the selected note."""
        index, *tag_list = args
        tag = " ".join(tag_list)
        real_index = int(index) - 1
        if not tag:
            return "Tag text is empty."
        if not 0 <= real_index < len(self.notes):
            return "No note found for this number."
        self.notes.delete_tag(real_index, tag)
        return "Tag deleted."

    @input_error
    def find_note_by_tag(self, args):
        """Find and list notes whose tag set contains the provided tag."""
        tag = " ".join(args)
        if not tag:
            return "Search tag is empty."
        matches = self.notes.find_by_tag(tag)
        if not matches:
            return f"No notes found for tag '{tag}'."
        return tabulate(
            matches,
            headers=["№", "Tags", "Note"],
            tablefmt="plain",
        )

    @input_error
    def show_notes_tag_sorted(self, reverse: bool = False):
        """Display all notes sorted by their tag string, asc by default."""
        if self.notes:
            rows = self.notes.sort_by_tag(reverse)
            return tabulate(
                rows,
                headers=["№", "Tags", "Note"],
                tablefmt="plain",
            )
        return "Notes are empty."

    @input_error
    def show_notes_tag_desc_sorted(self):
        """Display all notes sorted by tag string in descending order."""
        return self.show_notes_tag_sorted(reverse=True)

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
    def delete_contact(self, args):
        """Delete a contact entry from the address book."""
        name, *_ = args
        contact = self.book.delete(name)
        if contact is None:
            return f'Contact "{name}" does not exist.'
        return "Contact deleted."

    @input_error
    def add_email(self, args):
        """Attach a new email to an existing contact."""
        name, email, *_ = args
        contact = self.book.find(name)
        if contact is None:
            return f'Contact "{name}" does not exist.'
        if email:
            contact.add_email(email)
            return "Contact updated."
        else:
            return "Email is empty."

    @input_error
    def show_emails(self, args):
        """Display all emails saved for the selected contact."""
        name = args[0]
        contact = self.book.find(name)
        if contact is None:
            return f'Contact "{name}" does not exist.'
        if not contact.emails:
            return f'The contact "{name}" has no emails.'
        rows = [
            [contact.name.value, str(email)]
            for email in contact.emails
        ]
        return tabulate(
            rows,
            headers=["Name", "Email"],
            tablefmt="plain",
        )

    @input_error
    def change_email(self, args):
        """Replace an old contact email with a new value."""
        name, old_email, new_email, *_ = args
        contact = self.book.find(name)
        if contact is None:
            return f'Contact "{name}" does not exist.'
        if contact.find_email(old_email) is None:
            return f'Email "{old_email}" does not exist.'
        contact.edit_email(old_email, new_email)
        return "Contact updated."

    @input_error
    def set_address(self, args):
        """Set or update the free-form address for a contact."""
        name, *address_list = args
        address = " ".join(address_list)
        contact = self.book.find(name)
        if contact is None:
            return f'Contact "{name}" does not exist.'
        if address:
            contact.address = address
            return "Address updated."
        else:
            return "Address is empty."

    @input_error
    def change_phone(self, args):
        """Update the phone number for an existing contact."""
        name, old_phone, new_phone, *_ = args
        contact = self.book.find(name)
        if contact is None:
            return f'Contact "{name}" does not exist.'
        if contact.find_phone(old_phone) is None:
            return f'Phone "{old_phone}" does not exist.'
        contact.edit_phone(old_phone, new_phone)
        return "Contact updated."

    @input_error
    def show_phones(self, args):
        """Display the phone numbers for a specified contact."""
        name = args[0]
        contact = self.book.find(name)
        if contact is None:
            return f'Contact "{name}" does not exist.'
        if not contact.phones:
            return f'The contact "{name}" has no phones.'
        rows = [
            [contact.name.value, str(phone)]
            for phone in contact.phones
        ]
        return tabulate(
            rows,
            headers=["Name", "Phone"],
            tablefmt="plain",
        )

    def __get_contacts(self, contacts: List[Record]):
        """Convert contact objects to table rows with all key fields."""
        rows = []
        for contact in contacts:
            phones = "-"
            if contact.phones:
                phones = ", ".join(str(phone) for phone in contact.phones)

            emails = "-"
            if contact.emails:
                emails = ", ".join(str(email) for email in contact.emails)

            birthday = str(contact.birthday) if contact.birthday else "-"

            rows.append(
                [
                    contact.name.value,
                    birthday,
                    phones,
                    emails,
                    contact.address or "-",
                ]
            )
        return rows

    @input_error
    def search_contact(self, args):
        """Search contacts that match names, phones, or emails."""
        query = " ".join(args)
        if not query:
            return "Search query is empty."
        rows = self.__get_contacts(self.book.search(query))
        if not rows:
            return f"No contacts found for '{query}'."
        return tabulate(
            rows,
            headers=["Name", "Birthday", "Phones", "Emails", "Address"],
            tablefmt="plain",
        )

    @input_error
    def show_all(self):
        """Format and return a list of all contacts and their phone numbers."""
        rows = self.__get_contacts(self.book.data.values())
        if not rows:
            return "Address book is empty."
        return tabulate(
            rows,
            headers=["Name", "Birthday", "Phones", "Emails", "Address"],
            tablefmt="plain",
        )

    @input_error
    def add_birthday(self, args):
        """Add the birthday for an existing contact."""
        name, birthday, *_ = args
        contact = self.book.find(name)
        if contact is None:
            return f'Contact "{name}" does not exist.'
        contact.add_birthday(birthday)
        return "Contact birthday added."

    @input_error
    def show_birthday(self, args):
        """Display the birthday for a specified contact."""
        if not args:
            return "Contact name is empty."
        name = args[0]
        contact = self.book.find(name)
        if contact is None:
            return f'Contact "{name}" does not exist.'
        if contact.birthday is None:
            return "Contact date of birth is not specified."
        return str(contact.birthday)

    @input_error
    def show_birthdays(self, args):
        """Show birthdays that will occur within the next count_days."""
        if not args:
            return "Days count is required."
        count_days = args[0]
        if not count_days.isdigit():
            return "Days count must be a positive number."
        days = int(count_days)
        if days <= 0:
            return "Days count must be greater than zero."

        rows = [
            [congratulation.name, congratulation.congratulation_date]
            for congratulation in self.book.get_upcoming_birthdays(days)
        ]
        if not rows:
            return "No upcoming birthdays."
        return tabulate(
            rows,
            headers=["Name", "Congratulation date"],
            tablefmt="plain",
        )
