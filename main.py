from collections import UserDict
from datetime import datetime, date
import copy
import csv

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass
    
class Phone(Field):
    def __init__(self):
        self.__value = None

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        if len(new_value) == 10 and new_value.isdigit():
            self.__value = new_value
        else:
            raise ValueError('Wrong phone format!')
        
class Birthday(Field):
    def __init__(self):
        self.__value = None
    
    def __str__(self):
        return str(self.value.strftime("%d.%m.%Y"))

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        try:
            d = datetime.strptime(new_value, "%d.%m.%Y").date()
        except  ValueError:
            raise ValueError('Wrong date format!')    
        
        if d < date.today():
            self.__value = d
        else:
            raise ValueError('Date is in future!')        
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday =  None
        self.phones = []

    def add_phone(self, phone):
        p = Phone()
        p.value = phone
        self.phones.append(p)
    
    def add_birthday(self, birthday):
        self.birthday = Birthday()
        self.birthday.value = birthday

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

    def days_to_birthday(self):
        if self.birthday:
            d = self.birthday.value.replace(year=date.today().year)
            if d > date.today():
                delta = d - date.today()
                print(f"{delta.days} days to birthday")
            elif d < date.today():
                delta = self.birthday.value.replace(year=date.today().year + 1) - date.today()
                print(f"{delta.days} days to birthday")
            else:
                print(f"Happy birthday, {self.name.value}!")           

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value.strftime("%d.%m.%Y")}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
class AddressBook(UserDict):
           
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name not in self.data.keys():
            raise ValueError('Name not in Book')
        else:
            record = self.data[name]
            return record
                
    def delete(self, name):
        if name in self.data.keys():
            del self.data[name]
    
    def iterator(self, n=0):
        data = list(self.data.values())
        if n > len(data): 
            raise ValueError('Wrong num of records')
        i = 0
        while i < len(data):
            yield ' | '.join(str(item) for item in data[i:i+n])
            i += n   
    
    def save(self, filename):
        with open(filename, 'w', newline ='') as file:
            data=copy.deepcopy(list(self.data.values()))        # make  deep copy of list of book values 
            fieldsnames = vars(data[0]).keys()                  # set fileldsnames of csv file
            csv_writer = csv.DictWriter(file, fieldnames = fieldsnames, delimiter=';')
            csv_writer.writeheader()
            for row in data:
                phones = ','.join(str(phone) for phone in row.phones)    # change phone numbers to human readable view
                vars(row)['phones'] = phones
                csv_writer.writerow(rowdict=vars(row))
    
    def load(self, filename):
        with open(filename, 'r', newline ='') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                name_record = Record(f"{row['name']}")          #for every 'name' value  in row create Record object
                for item in row['phones'].split(','):           #for every phone in 'phones' value add Phone objects to Record
                    name_record.add_phone(f'{item}')            
                if row['birthday'] != '':                       #add 'birthday' value if exists to Record 
                    name_record.add_birthday(row['birthday'])
                self.add_record(name_record)                    #add Record to Book
        return self
    
    def findall(self, value=''):
        for item in list(self.data.values()):                   
            name_str = item.name.value                          #get str value name
            phone_str = ','.join(str(phone) for phone in item.phones)  #get str value phones
            if name_str.find(value) != -1 or phone_str.find(value) != -1:   #find in str values
                print(item)


book = AddressBook()
names1 = ["asd","qwe",]
names2 = ["asdfg","qwerty"]
for name in names1:
    name_record = Record(f"{name}")
    name_record.add_phone("1111111111")
    name_record.add_phone("2222222222")
    name_record.add_birthday("10.01.1985")
    book.add_record(name_record)
for name in names2:
    name_record = Record(f"{name}")
    name_record.add_phone("1234567890")
    name_record.add_phone("0987654321")
    book.add_record(name_record)

# for name, record in book.data.items():
#     print(record)
# print('----------------')

# # a = book.find('a')
# # a.days_to_birthday()
# # print('----------------')

# # for i in book.iterator(2):
# #     print(i)

# #print(book)
book.save('book.csv')
book1 = AddressBook()
book1.load('book.csv')
#c = book1.find('c')
#c.add_birthday("10.01.1986")
book1.save('book.csv')
# for name, record in book1.data.items():
#     print(record)
book1.findall('asdf')