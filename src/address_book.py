"""Core data structures for storing contacts, notes, and search logic."""

from collections import UserDict
from datetime import datetime, date
from typing import List
import re


class Field:
    """Base class for typed value objects with common validation hooks."""

    def __init__(self, value):
        """Create a field and immediately validate the provided value."""
        self._value = None
        self.value = value

    @property
    def value(self):
        """Return the stored primitive value."""
        return self._value

    @value.setter
    def value(self, value):
        """Assign the field value; subclasses may override for validation."""
        self._value = value

    def __str__(self):
        """Convert the value to string for display purposes."""
        return str(self.value)


class Name(Field):
    """Simple wrapper around the contact name value."""


class Phone(Field):
    """Field responsible for validating and storing phone numbers."""
    def __init__(self, value: str):
        """Validate and store a phone consisting of exactly 12 digits."""
        if not isinstance(value, str):
            raise ValueError("Phone number must be a string")
        cleaned_value = value.strip()
        if cleaned_value.isdigit() and len(cleaned_value) == 12:
            super().__init__(cleaned_value)
            return
        raise ValueError("Phone must contain 12 characters and only numbers")


class Email(Field):
    """Field that validates and stores email values."""
    def __init__(self, value: str):
        """Validate email value using a basic regex before storing."""
        if not isinstance(value, str):
            raise ValueError("Email must be a string")
        cleaned_value = value.strip()
        regex_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if re.fullmatch(regex_pattern, cleaned_value, flags=re.IGNORECASE):
            super().__init__(cleaned_value)
            return
        raise ValueError("Invalid email.")


class Birthday(Field):
    """Field that stores birthday dates as `datetime.date` objects."""
    def __init__(self, value: str):
        """Parse a birthday string and ensure it is not a future date."""
        try:
            birthday_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError as exc:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from exc
        if birthday_date > datetime.now().date():
                raise ValueError("Date must be in the past.")
        super().__init__(birthday_date)

    def __str__(self):
        """Return the birthday formatted back to DD.MM.YYYY."""
        return self.value.strftime("%d.%m.%Y")


class Record:
    """Represents a contact and aggregates all related details."""
    def __init__(self, name: str):
        """Initialize a contact record with optional detail containers."""
        self.name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Birthday = None
        self.address: str = None
        self.emails: List[Email] = []

    def add_phone(self, phone_number: str) -> None:
        """Attach a unique phone to the record."""
        for phone in self.phones:
            if phone_number == str(phone):
                return
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        """Remove a matching phone number if it exists."""
        for index, phone in enumerate(self.phones):
            if phone_number == str(phone):
                self.phones.pop(index)

    def edit_phone(self, old_phone_number: str, new_phone_number: str) -> None:
        """Replace an existing phone with a new value."""
        for index, phone in enumerate(self.phones):
            if old_phone_number == str(phone):
                self.phones[index] = Phone(new_phone_number)

    def find_phone(self, phone_number: str) -> str | None:
        """Return the stored phone string if it exists."""
        for phone in self.phones:
            if phone_number == str(phone):
                return phone_number

    def add_email(self, email_value: str) -> None:
        """Attach a unique email address to the record."""
        for email in self.emails:
            if email_value == str(email):
                return
        self.emails.append(Email(email_value))

    def remove_email(self, email_value: str) -> None:
        """Delete an email address if present."""
        for index, email in enumerate(self.emails):
            if email_value == str(email):
                self.emails.pop(index)

    def edit_email(self, old_email_value: str, new_email_value: str) -> None:
        """Replace an existing email with a new one."""
        for index, email in enumerate(self.emails):
            if old_email_value == str(email):
                self.emails[index] = Email(new_email_value)

    def find_email(self, email_value: str) -> str | None:
        """Return an email string if the record contains it."""
        for email in self.emails:
            if email_value == str(email):
                return email_value

    def add_birthday(self, birthday_value: str) -> None:
        """Assign a birthday to the contact."""
        self.birthday = Birthday(birthday_value)

    def __str__(self):
        """Provide a human-readable dump of the record fields."""
        return f"Contact name: {self.name.value}, \
            address: {self.address} \
            phones: {'; '.join(p.value for p in self.phones)} \
            emails: {'; '.join(p.value for p in self.emails)}"


class Congratulation:
    """Helper object describing when to congratulate a contact."""
    def __init__(self, name: str, congratulation_date: str):
        """Store a congratulation reminder for a specific date."""
        self.name = name
        self.congratulation_date = congratulation_date

    def __str__(self):
        """Return a short label with name and congratulation date."""
        return f"{self.name}: {self.congratulation_date}"

    def __repr__(self):
        """Return a debug-friendly representation for the reminder."""
        return f"Congratulation(name = \"{self.name}\"" \
            ", congratulation_date = \"{self.congratulation_date}\")"


class AddressBook(UserDict):
    """Dictionary-like container that manages contact records."""
    def add_record(self, contact_record: Record) -> None:
        """Store or replace a contact by its name key."""
        self.data[str(contact_record.name)] = contact_record

    def find(self, name: str) -> Record | None:
        """Return the contact record matching the provided name."""
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name: str) -> Record | None:
        """Remove a contact entry and return it if found."""
        if name in self.data:
            return self.data.pop(name)

    def __get_birthday_this_year(self, birthday, year) -> None:
        """Return a date object for this year's birthday (handles leap years)."""
        try:
            return date(year, birthday.month, birthday.day)
        except ValueError:
            if birthday.month == 2 and birthday.day == 29:
                return date(year, 2, 28)
            return None

    def __get_next_birthday(self, birthday, today):
        """Determine the next birthday date relative to `today`."""
        birthday_this_year = self.__get_birthday_this_year(birthday, today.year)
        if birthday_this_year and birthday_this_year >= today:
            return birthday_this_year
        birthday_next_year = self.__get_birthday_this_year(birthday, today.year + 1)
        return birthday_next_year

    def get_upcoming_birthdays(self, count_days: int = 7) -> List[Congratulation]:
        """Collect congratulation reminders for birthdays within the window."""
        today = datetime.today().date()
        result: List[Congratulation] = []

        for name in self.data:
            contact_record = self.data[name]
            if not isinstance(contact_record.birthday, Birthday):
                continue
            birthday = contact_record.birthday.value
            if not birthday:
                continue

            birthday_date = self.__get_next_birthday(birthday, today)
            if not birthday_date:
                continue

            delta_days = (birthday_date - today).days
            if 0 <= delta_days <= count_days:
                result.append(Congratulation(name, birthday_date.strftime("%d.%m.%Y")))

        return result

    def search(self, query: str):
        """Find contacts whose name, phone, or email contains the query."""
        contacts = []
        for contact_record in self.data.values():
            if query.lower() in contact_record.name.value.lower():
                contacts.append(contact_record)
                continue
            contact_by_phone = None
            for phone in contact_record.phones:
                if query in phone.value:
                    contact_by_phone = contact_record
                    break
            if contact_by_phone:
                contacts.append(contact_by_phone)
                continue
            for email in contact_record.emails:
                if query.lower() in email.value.lower():
                    contacts.append(contact_record)
                    break
        return contacts


if __name__ == "__main__":
# Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("123456789012")
    john_record.add_phone("555555555512")
    john_record.add_email("tttt@gmail.com")
    john_record.add_email("bbb@gmail.com")
    john_record.address = "address address address"
    john_record.add_birthday("03.11.1985")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("987654321012")
    jane_record.add_birthday("05.11.2000")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for contact in book.data.values():
        print(contact)

    print(book.get_upcoming_birthdays())
    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("123456789012", "111222333312")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("555555555512")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
