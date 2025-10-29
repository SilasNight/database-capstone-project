import sqlite3

BOOKS_DATABASE = "ebookstore.db"


def check_databases() -> None:
    """
    Used to make sure that all the database tables exist.
    :return: None
    """
    db = sqlite3.connect(BOOKS_DATABASE)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS books ("
                   "id text PRIMARY KEY,"
                   "title text,"
                   "authorID text,"
                   "qty int"
                   ");")
    cursor.close()
    db.close()

def append_books(data):
    pass


def add_new_book():
    pass


def yes_or_no() -> bool:
    """
    This function is used to ask the user a yes or no question
    and return a True or False as the outcome
    :return: True or False
    """

    user_input = ""
    options = ["Yes", "No", "Y", "N"]

    # Locking the user in until one of the answers are given
    while user_input not in options:
        user_input = input("Please select (Yes/No)\n").title()

    # Note I check only for the 'Y' and change it to 'Yes'
    if user_input == "Y":
        user_input = "Yes"

    # As I checked for the 'Y' Earlier there is only one positive option.
    if user_input == "Yes":
        return True
    else:
        return False


def main_menu() -> str:
    """
    This is used to get specific strings for the menu
    :return: string
    """
    user_input = ''

    # Making a list of possible options that is easily editable
    options = [
        "Add",
        "Update",
        "Delete",
        "Search",
        "Exit",
    ]

    while user_input not in options:
        print("\nThis is the main menu")
        for option in options:
            print(option)
        user_input = input("Please choose one on the above.\n").title()

    return user_input

check_databases()
while True:
    action = main_menu()
    match action:
        case "Add":
            pass
        case "Update":
            pass
        case "Delete":
            pass
        case "Search":
            pass
        case "Exit":
            print("Have a nice day")
            break
