from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass
    
class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise ValueError

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        p = Phone(phone)
        self.phones.append(p)
    
    def edit_phone(self, phone, new_phone):
        if phone not in [p.value for p in self.phones]:
            raise ValueError
        for i in range(len(self.phones)):
            if self.phones[i].value == phone:
                self.phones[i].value = new_phone
                return self.phones        
    
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
    
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p) 

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        if name in self.data.keys():
            record = self.data[name]
            return record
                
    def delete(self, name):
        if name in self.data.keys():
            del self.data[name]
