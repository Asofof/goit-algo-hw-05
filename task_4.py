# Этот декоратор оборачивает функции, обрабатывая возможные ошибки
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "This contact does not exist." # если запрашиваемый контакт отсутствует
        except ValueError:
            return "Give me name and phone please." # если передано недостаточно аргументов
        except IndexError:
            return "Enter the argument for the command." # если аргументы не переданы
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error # додамо декоратор
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error # додамо декоратор
def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        raise KeyError # В случае отсутствия контакта вызывает исключение KeyError, и декоратор возвращает "This contact does not exist."

@input_error # додамо декоратор
def show_phone(args, contacts):
    name = args[0]
    return contacts[name] # Если контакта нет, выбрасывает KeyError.

def show_all(contacts):
    if not contacts:
        return "No contacts saved."
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:  # Проверяем, введена ли пустая строка
            print("Please enter a valid command.")
            continue
        command, args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
