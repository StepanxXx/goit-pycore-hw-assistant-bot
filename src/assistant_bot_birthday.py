from collections import UserDict
from datetime import timedelta, datetime
from functools import wraps
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Ім'я не може бути порожнім")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Телефон має містити рівно 10 цифр")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return True
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value}"if self.birthday else""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                bday_this_year = bday.replace(year=today.year)

                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)

                days_diff = (bday_this_year - today).days
                if 0 <= days_diff <= 6:
                    congratulation_date = bday_this_year
                    if congratulation_date.weekday() == 5:  # субота
                        congratulation_date += timedelta(days=2)
                    elif congratulation_date.weekday() == 6:  # неділя
                        congratulation_date += timedelta(days=1)
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })
        return upcoming_birthdays


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Помилка: {e}"
    return inner


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        return "Вкажіть ім'я та день народження y форматі DD.MM.YYYY"
    name, birthday = args[0], args[1]
    record = book.find(name)
    if not record:
        return f"Контакт з ім'ям {name} не знайдено"
    try:
        record.add_birthday(birthday)
        return f"День народження для {name} додано: {birthday}"
    except ValueError as e:
        return f"Помилка: {e}"


@input_error
def show_birthday(args, book):
    if not args:
        return "Вкажіть ім'я контакту"
    name = args[0]
    record = book.find(name)
    if not record:
        return f"Контакт з ім'ям {name} не знайдено"
    if not record.birthday:
        return f"Для {name} день народження не вказано"
    return f"День народження {name}: {record.birthday.value}"


@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "Немає користувачів з днями народження на наступному тижні"
    result = "Вітаємо наступних користувачів:\n"
    for item in upcoming:
        result += f"{item['name']}: {item['congratulation_date']}\n"
    return result.strip()


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phones(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()
    while True:
        command = input("Enter a command: ")
        if command == "exit":
            save_data(book)
            print("Address book saved. Goodbye!")
            break


if __name__ == "__main__":
    main()