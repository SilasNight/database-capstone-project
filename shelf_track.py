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


def update_books_database(data: list) -> None:
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
    command = (f"UPDATE {BOOKS_DATABASE} "
               f"SET title = '{title}', authorID = {author_id}, qty = {quantity} "
               f"WHERE id = {book_id};")

    cursor.execute(command)
    db.commit()

    # Close the connection
    cursor.close()
    db.close()


def update_books() -> None:
    """
    This is used to update a book that is already in the database
    :return: Nothing
    """

    # Loading needed data and showing a list of books
    data = load_books()
    view_all_books()

    # Getting the index of the book the user wants to edit
    index = get_digit(constraint=len(data), question="Type in the number of the"
                                                     " book would you like to edit?\n")

    # Getting the selected book and displaying it
    book_to_edit = data[index-1]
    to_display = format_book_data([book_to_edit])
    for line in to_display:
        print(line)

    # Getting the new values for the book
    if yes_or_no(question=f"Do you want to change the title ({book_to_edit[1]})"):
        new_title = get_book_title(book_to_edit[1])
    else:
        new_title = book_to_edit[1]

    if yes_or_no(f"({book_to_edit[2]}) is the old auther ID. Do you want to change it?"):
        new_author_id = get_id()
    else:
        new_author_id = book_to_edit[2]

    if yes_or_no(f"Do you want to change the quantity :{book_to_edit[3]}"):
        new_quantity = get_digit(question="How many books are there now?\n")
    else:
        new_quantity = book_to_edit[3]

    updated_book = [book_to_edit[0], new_title, new_author_id, new_quantity]

    # Giving the data to the other function to update the database.
    update_books_database(updated_book)
    print(f"Book {index} has been updated.")


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
    book_id = get_id(question="Please type in the books ID\n")
    title = get_book_title()
    author_id = get_id(question="Please type in the authors ID\n")
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


def get_id(question: str = None) -> str:
    """
    This is used to get a valid number ID
    :param question: This will be asked to the user
    :return: a string of whole numbers
    """

    # Changing the question based on the type of ID required.
    if question:
        query = question
    else:
        query = "Please type in the ID. It must be a number.\n"

    satisfied = False
    user_input = ''
    while not satisfied:
        user_input = input(query)

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


def yes_or_no(question: str = None) -> bool:
    """
    This function is used to ask the user a yes or no question
    and return a True or False as the outcome
    :return: True or False
    """

    user_input = ""
    options = ["Yes", "No", "Y", "N"]

    if question:
        print(question)

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


def view_all_books() -> None:
    """
    This is used to display all the data from the books table.
    :return: None
    """
    data = load_books()

    data = format_book_data(data)

    # Then prints it all out all at once
    for line in data:
        print(line)


def format_book_data(data: list) -> list:
    """
    This is used to format books regardless of how many there are.
    :param data: This has to be a list of lists.
    :return: a list of strings meant to be displayed.
    """

    book_data_labels = [
        "Book ID",
        "Book Title",
        "Author ID",
        "Quantity"
    ]

    books_data = [""]
    counter = 0

    # This is formating all the data into an easy-to-read string
    for book in data:
        counter += 1
        books_data.append(f"Book: {counter}")
        for i in range(len(book)):
            string = f"{book_data_labels[i].ljust(11)}: {book[i]}"
            books_data.append(string)
        books_data.append("")

    return books_data


def load_books() -> list:
    """
    Loading all the data from the books table and turning it into a
    list of lists.
    :return: list of books data in a list
    """

    # Connecting to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # Getting all the data
    cursor.execute(f"SELECT * FROM {BOOKS_DATABASE};")
    data = cursor.fetchall()

    cursor.close()
    db.close()

    # Making it a list of lists which is easier to use.
    data = [list(x) for x in data]
    return data


def search_books() -> None:
    """
    This shows the user the ID's off all the books stored and
    lets them look for any ID and then displays that book if there is a match
    :return: Nothing.
    """

    # Loading relevant data
    data = load_books()
    book_ids = [x[0] for x in data]

    while True:

        # Listing all the ID's
        print("These are the searchable book IDs")
        for ID in book_ids:
            print(ID)

        # Making sure that the user want's to search after
        # being shown all the ID's
        print("Would you like to search?")
        if yes_or_no():

            # Using the function to get a valid ID from the user
            user_input = get_id(question="Please type in an ID to search for.\n")
        else:
            print("Going back to main menu")
            break

        # If the user entered an ID that is in the database it is displayed.
        if user_input in book_ids:
            print("Book Found.\n")
            for book in data:
                if book[0] == user_input:
                    book = format_book_data([book])
                    for line in book:
                        print(line)
                    break
        else:
            print("ID doesn't match id's in the system.")


def main_menu() -> str:
    """
    This is used to get specific strings for the menu
    :return: string
    """
    user_input = ''

    # Making a list of possible options that is easily editable
    options = [
        "View",
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
        case "View":
            view_all_books()
        case "Add":
            add_new_book()
        case "Update":
            update_books()
        case "Delete":
            pass
        case "Search":
            search_books()
        case "Exit":
            print("Have a nice day")
            break
