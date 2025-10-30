import sqlite3

DATABASE = "ebookstore.db"
BOOKS_DATABASE = "books"


def check_databases() -> None:
    """
    Used to make sure that all the database tables exist.
    :return: None
    """
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {BOOKS_DATABASE} ("
                   "id text PRIMARY KEY,"
                   "title text,"
                   "authorID text,"
                   "qty int"
                   ");")
    cursor.close()
    db.close()


def update_books(data: list) -> None:
    """
    This is used to update the books table in the database.
    :param data: list of data to be overwritten.
    :return: None
    """

    # Set up connection
    book_id, title, author_id, quantity = data
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # Update the data and save
    cursor.execute(f"UPDATE {BOOKS_DATABASE}"
                   f"SET title = {title}, authorID = {author_id}, qty = {quantity}"
                   f"WHERE id = {book_id}")
    db.commit()

    # Close the connection
    cursor.close()
    db.close()


def append_books(data: list) -> None:
    """
    This is used to append new data to books table
    :param data: list of data to add
    :return: None
    """

    # Set up the connection
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # Add it and save
    cursor.execute(f"INSERT INTO {BOOKS_DATABASE}(id, title, authorID, qty)"
                   f"VALUES(?, ?, ?, ?);", tuple(data))
    db.commit()

    # Close the connection
    cursor.close()
    db.close()


def add_new_book() -> None:
    """
    This is used to gather all the information of a new book
    It will later call a different function to add the data to
    The books database
    :return: None
    """

    print("Now adding a new book")

    # Gathering the data
    book_id = get_id()
    title = get_book_title()
    author_id = get_id()
    quantity = get_digit(question="How many books are you adding?\n")

    # Condensing all the data and adding it to the database
    data = [book_id, title, author_id, quantity]
    append_books(data)


def get_book_title(old_title: str = None) -> str:
    """
    This is used to get the title of a book.
    Can be used to edit an existing title as well.
    :return: str The title of the book.
    """
    while True:

        # Checking if there is an old title to show as polish
        if old_title:
            print(f"The old title was: {old_title}")

        # Keeping the user trapped in this loop until they confirm
        # That they are happy with the book title.
        user_input = input("What should the title for the book be?\n").title()
        print(f"Is this correct: {user_input}")
        if yes_or_no():
            return user_input


def get_id() -> str:
    """
    This is used to get a valid number ID
    :return: a string of whole numbers
    """

    satisfied = False
    user_input = ''
    while not satisfied:
        user_input = input("Please type in the ID. It must be a number.\n")

        # Making sure that the user has input something.
        if len(user_input) == 0:
            print("Something must be entered.")
            continue

        # Making sure that the whole string is numbers.
        for i in range(len(user_input)):
            if not user_input[i].isdigit():
                print(f"Character {i+1} is not a number")
                continue

        satisfied = True
    return user_input


def get_digit(constraint: int = None, question: str = None) -> int:
    """
    This function is used to get a positive whole number.
    If there is a constraint it makes it so that the number has to be
    smaller than the constraint.

    :param question: This is a changeable question to ask
    inside the function
    :param constraint: A limit to how big the number can be.
    :return: integer selected
    """

    # Changing the question based on it's existence
    if question:
        prompt = question
    else:
        prompt = "Please enter a positive whole number.\n"

    potential_output = 0
    while True:
        user_input = input(prompt)

        # Making sure it is a valid number and not negative.
        if not user_input.isdigit():
            print(f"Error, {user_input} is not a positive whole number.")
            continue

        # Changing the input to int for more testing
        potential_output = int(user_input)
        if potential_output == 0:
            print("Error the number can't be equal to zero.")
            continue

        # If there is a constraint this tests it.
        if constraint:
            if potential_output > constraint:
                print(f"Error the number must be equal or less than {constraint}")
                continue
        break

    return potential_output


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

    # Printing out the current accepted options and
    # keeping the user trapped until one is selected
    while user_input not in options:
        print("\nThis is the main menu")
        for i in range(len(options)):
            print(f"{i+1}. {options[i]}")
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
