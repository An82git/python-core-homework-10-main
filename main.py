from collections import UserDict


contacts = {}
ERROR_DIC = {"add_IndexError": "Give me name and phone please",
             "change_IndexError": "Give me name and phone please",
             "phone_IndexError": "Enter user name",
             "phone_KeyError": "There is no such name",
             "phone_ValueError": "Wrong phone number"}

class Field:
    def __init__(self, value: str):
        if value[0] not in "0123456789":
            self.value = value.title()
        else:
            self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, phone: str):
        if len(phone) == 10 and phone.isnumeric():
            super().__init__(phone)
        else:
            raise ValueError

class Record:
    def __init__(self, name: str, phone: str | list = []):
        self.name = Name(name)
        self.phones = [Phone(p) for p in phone] if type(phone) == list else [Phone(phone)]

    # реалізація класу
    def add_phone(self, phone: str): # додавання Phone
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str): # видалення Phone
        index_phone = [str(p) for p in self.phones].index(phone)
        self.phones.pop(index_phone)

    def edit_phone(self, old_phone: str, new_phone: str): # редагування Phone
        index_phone = [str(p) for p in self.phones].index(old_phone)
        self.phones.pop(index_phone)
        self.phones.insert(index_phone, Phone(new_phone))

    def find_phone(self, phone: str) -> Phone: # пошуку Phone
        for p in self.phones:
            if str(p) == phone:
                return p

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    # реалізація класу
    data = {}

    def add_record(self, record: Record): # який додає запис до self.data
        self.data.update({record.name.value: record})

    def find(self, name: str) -> Record: # знаходить запис за ім'ям
        for n in self.data:
            if name.title() == n:
                return self.data.get(n)

    def delete(self, name: str): # видаляє запис за ім'ям
        for n in self.data:
            if name.title() == n:
                self.data.pop(n)
                return 


def hello() -> str:
    return "How can I help you?"


def add(name: str, phone: str):
    return contacts.update({name.title(): phone})


def change(name: str, phone: str):
    return contacts.update({name.title(): phone})


def phone(name: str) -> str:
    return contacts[name.title()]


def show_all() -> dict:
    return contacts


def good_bye() -> str:
    return "Good bye!"


def close() -> str:
    return "Good bye!"


def exit() -> str:
    return "Good bye!"


COMMAND_DIC = {"hello": hello,
               "add": add,
               "change": change,
               "phone": phone,
               "show all": show_all,
               "good bye": good_bye,
               "close": close,
               "exit": exit}


def input_error(func):
    def inner(string: str):
        try:
            return func(string)

        except IndexError:
            command_error = pars(string)

            if not command_error:
                return "A non-existent team"
            elif command_error[0] + "_IndexError" in ERROR_DIC:
                return ERROR_DIC[command_error[0] + "_IndexError"]
            return "Unknown error"

        except KeyError:
            command_error = pars(string)

            if command_error[0] + "_KeyError" in ERROR_DIC:
                return ERROR_DIC[command_error[0] + "_KeyError"]
            return "A non-existent team"
        
        except ValueError:
            command_error = pars(string)

            if command_error[0] + "_ValueError" in ERROR_DIC:
                return ERROR_DIC[command_error[0] + "_KeyError"]

    return inner


@input_error
def command_processing(data: AddressBook, string: str):
    string_list = pars(string)
    command = COMMAND_DIC[string_list[0]]

    if string_list[0] in ["add"]:
        return command(data, string_list[1], string_list[2])
    elif string_list[0] in ["change"]:

        if string_list[1].title() not in contacts:
            return "There is no such name"

        return command(data, string_list[1], string_list[2])
    elif string_list[0] in ["phone"]:
        return command(string_list[1])
    else:
        return command()


def pars(string: str) -> list:
    string_list = []
    string = string.strip()

    for command in COMMAND_DIC:
        if command in string:
            string_list.append(command)
            string = string.removeprefix(command).strip()

    if string:
        for item in string.split(" "):
            if item[0] in "+0123456789":
                string_list.insert(2, item)
            else:
                string_list.insert(1, item)

    return string_list


def main():
    end_of_program = True

    book = AddressBook()

    while end_of_program:
        string = input().lower()

        if string:
            rezult_command = command_processing(string)

            
            if type(rezult_command) in [dict]:
                for name, record in book.data.items():
                    print(record)
            elif type(rezult_command) in [str]:
                print(rezult_command)

                if rezult_command == "Good bye!":
                    end_of_program = False

        else:
            end_of_program = False


if __name__ == "__main__":
    main()
