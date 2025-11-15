from collections import UserDict
from datetime import datetime, date, timedelta
from typing import List

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Phone number must be a string")
        cleaned_value = value.strip()
        if cleaned_value.isdigit() and len(cleaned_value) == 10:
            self._value = cleaned_value
            super().__init__(cleaned_value)
            return
        raise ValueError("Phone must contain 10 characters and only numbers")

class Birthday(Field):
    def __init__(self, value: str):
        try:
            birthday_date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(birthday_date)
        except ValueError as exc:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from exc
    
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number: str) -> None:
        for phone in self.phones:
            if phone_number == str(phone):
                return
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        for index, phone in enumerate(self.phones):
            if phone_number == str(phone):
                self.phones.pop(index)

    def edit_phone(self, old_phone_number: str, new_phone_number: str) -> None:
        for index, phone in enumerate(self.phones):
            if old_phone_number == str(phone):
                self.phones[index] = Phone(new_phone_number)

    def find_phone(self, phone_number: str) -> str | None:
        for phone in self.phones:
            if phone_number == str(phone):
                return phone_number

    def add_birthday(self, birthday_value: str) -> None:
        self.birthday = Birthday(birthday_value)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class Congratulation:
    def __init__(self, name: str, congratulation_date: str):
        self.name = name
        self.congratulation_date = congratulation_date
    
    def __str__(self):
        return f"{self.name}: {self.congratulation_date}"
    
    def __repr__(self):
        return f"Congratulation(name = \"{self.name}\", congratulation_date = \"{self.congratulation_date}\")"

class AddressBook(UserDict):
    def add_record(self, contact: Record) -> None:
        self.data[str(contact.name)] = contact

    def find(self, name: str) -> Record | None:
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name: str) -> None:
        if name in self.data:
            self.pop(name)

    def __get_birthday_this_year(self, birthday, year) -> None:
        try:
            return date(year, birthday.month, birthday.day)
        except ValueError:
            if birthday.month == 2 and birthday.day == 29:
                return date(year, 2, 28)
            return None

    def __get_next_birthday(self, birthday, today):
        birthday_this_year = self.__get_birthday_this_year(birthday, today.year)
        if birthday_this_year and birthday_this_year >= today:
            return birthday_this_year
        birthday_next_year = self.__get_birthday_this_year(birthday, today.year + 1)
        return birthday_next_year

    def __get_congratulation_date(self, birthday_date):
        weekday = birthday_date.weekday()
        if weekday >= 5:
            days_to_monday = 7 - weekday
            return birthday_date + timedelta(days=days_to_monday)
        return birthday_date

    def get_upcoming_birthdays(self) -> List[Congratulation]:
        today = datetime.today().date()
        result: List[Congratulation] = []

        for name in self.data:
            contact = self.data[name]
            if not isinstance(contact.birthday, Birthday):
                continue
            birthday = contact.birthday.value
            if not birthday:
                continue

            birthday_date = self.__get_next_birthday(birthday, today)
            if not birthday_date:
                continue

            delta_days = (birthday_date - today).days
            if 0 <= delta_days <= 7:
                congratulation = self.__get_congratulation_date(birthday_date)
                result.append(Congratulation(name, congratulation.strftime("%d.%m.%Y")))

        return result


if __name__ == "__main__":
# Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("03.11.1985")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("05.11.2000")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for record in book.data.values():
        print(record)

    print(book.get_upcoming_birthdays())
    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
