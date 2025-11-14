"""Command handler class for the assistant bot."""

from tabulate import tabulate
from src.notes import Notes
from src.address_book import AddressBook, Record
from src.input_error import input_error


class AssistantBotHandlers:
    """Encapsulates the contact management operations."""

    def __init__(self, book: AddressBook, notes: Notes) -> None:
        self.book = book
        self.notes = notes    

    @input_error
    def add_note(self, args):
        note = " ".join(args)
        if not note:
            return "Note is empty."
        self.notes.add(note)
        return "Note added."

    @input_error
    def show_notes(self):
        if self.notes:
            rows = [[key + 1, note] for key,note in enumerate(self.notes)]
            return tabulate(rows, headers=["№","Note"], tablefmt="plain")
        return "Notes are empty."

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
        name, *_ = args
        contact = self.book.delete(name)
        if contact is None:
            return f"Contact \"{name}\" is not exists."
        return "Contact deleted."
    
    @input_error
    def add_email(self, args):
        name, email, *_ = args
        contact = self.book.find(name)
        if contact is None:
            return "Contact is not exists."
        if email:
            contact.add_email(email)
            return "Contact updated."
        else:
            return "Email is empty."
    
    @input_error
    def show_emails(self, args):
        name = args[0]
        contact = self.book.find(name)
        if contact is None:
            return f'Contact "{name}" is not exists.'
        if len(contact.emails) <= 0:
            return f'The contact "{name}" has no emails.'
        rows = [[contact.name.value, str(email)] for email in contact.emails]
        return tabulate(rows, headers=["Name", "Email"], tablefmt="plain")

    @input_error
    def change_email(self, args):
        name, old_email, new_email, *_ = args
        contact = self.book.find(name)
        if contact is None:
            return f'Contact "{name}" is not exists.'
        if contact.find_email(old_email) is None:
            return f'Email "{old_email}" is not exists.'
        contact.edit_email(old_email, new_email)
        return "Contact updated."

    @input_error
    def set_address(self, args):
        name, *address_list = args
        address = " ".join(address_list)
        contact = self.book.find(name)
        if contact is None:
            return "Contact is not exists."
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
            return f'Contact "{name}" is not exists.'
        if contact.find_phone(old_phone) is None:
            return f'Phone "{old_phone}" is not exists.'
        contact.edit_phone(old_phone, new_phone)
        return "Contact updated."

    @input_error
    def show_phones(self, args):
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
            emails = ", ".join(str(email) for email in contact.emails) if contact.emails else "-"
            rows.append([contact.name.value, birthday, phones, emails, contact.address or "-"])
        if not rows:
            return "Address book is empty."
        return tabulate(rows, headers=["Name", "Birthday", "Phones", "Emails", "address"], tablefmt="plain")

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
        if not args:
            return 'Contact name is empty.'
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
