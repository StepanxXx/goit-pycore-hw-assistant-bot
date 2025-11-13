class Record:
    def __init__(self, name, address=None, birthday=None):
        self.name = Name(name)
        self.address = Address(address) if address else None
        self.phones = []
        self.emails = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_email(self, email):
        self.emails.append(Email(email))

    def edit_phone(self, old, new):
        for idx, p in enumerate(self.phones):
            if p.value == old:
                self.phones[idx] = Phone(new)
                return True
        return False

    def edit_email(self, old, new):
        for idx, e in enumerate(self.emails):
            if e.value == old:
                self.emails[idx] = Email(new)
                return True
        return False

    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = ', '.join(p.value for p in self.phones)
        emails = ', '.join(e.value for e in self.emails)
        address = f", адреса: {self.address.value}" if self.address else ""
        birthday = f", день народження: {self.birthday.value}" if self.birthday else ""
        return f"Ім'я: {self.name.value}{address}, телефони: {phones}, email: {emails}{birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, query):
        # Пошук за іменем, телефоном, email або адресою
        results = []
        for rec in self.data.values():
            if (query.lower() in rec.name.value.lower() or
                any(query in p.value for p in rec.phones) or
                any(query in e.value for e in rec.emails) or
                (rec.address and query.lower() in rec.address.value.lower())):
                results.append(rec)
        return results

    def delete(self, name):
        return self.data.pop(name, None)
