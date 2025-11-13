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