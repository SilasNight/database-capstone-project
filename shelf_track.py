import sqlite3

DATABASE = "ebookstore.db"
BOOKS_TABLE = "books"
AUTHORS_TABLE = "author"


def check_databases() -> None:
    """
    Used to make sure that all the database tables exist.
    :return: None
    """
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute(f"CREATE TABLE IF NOT EXISTS {BOOKS_TABLE} ("
                   "id text PRIMARY KEY, "
                   "title text, "
                   "authorID text, "
                   "qty int"
                   ");")

    cursor.execute(f"CREATE TABLE IF NOT EXISTS {AUTHORS_TABLE} ("
                   "id text PRIMARY KEY, "
                   "name text, "
                   "country text"
                   ");")

    cursor.close()
    db.close()


def load_authors() -> list | bool:
    """
    This function is used to load all the data in the
    authors table
    :return: List of data from the
    """

    # Create a connection and get all the data from the table
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {AUTHORS_TABLE}")
    data = cursor.fetchall()

    # Switching the data to list to make it easier to work with
    if len(data) != 0:
        data = [list(x) for x in data]
    else:
        return False

    cursor.close()
    db.close()

    return data


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
    command = (f"UPDATE {BOOKS_TABLE} "
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
    if data:
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
    else:
        print("There are no books to update.")


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
    cursor.execute(f"INSERT INTO {BOOKS_TABLE}(id, title, authorID, qty)"
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

    data = load_books()
    book_ids = 0
    if data:
        book_ids = [x[0] for x in data]

    print("Now adding a new book")

    # Gathering the data
    while True:
        book_id = get_id(question="Please type in the books ID\n")
        if data:
            if book_id in book_ids:
                print("That book ID is already used")
            else:
                break
        else:
            break

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

    if data:
        data = format_book_data(data)

        # Then prints it all out all at once
        for line in data:
            print(line)
    else:
        print("No books to view.")


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


def load_books() -> list | bool:
    """
    Loading all the data from the books table and turning it into a
    list of lists.
    Also Checks if there is data to return.
    :return: list of books data in a list
    """

    # Connecting to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # Getting all the data
    cursor.execute(f"SELECT * FROM {BOOKS_TABLE};")
    data = cursor.fetchall()

    cursor.close()
    db.close()

    # Making it a list of lists which is easier to use.
    if len(data) == 0:
        return False
    else:
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

    if data:
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
    else:
        print("There are no books available to search through.")


def delete_book():
    """
    Function to select the book to be deleted
    with the aid of a different function it deleted the
    record from the database
    :return: None
    """

    data = load_books()
    if data:
        view_all_books()

        index = get_digit(len(data), "Select which book you would "
                                     "like to delete by number.\n")

        book_to_delete = data[index-1]
        book_id_to_delete = book_to_delete[0]

        if yes_or_no("Are you sure you want to delete the book?"):
            delete_from_database(book_id_to_delete)
    else:
        print("There are no books to delete.")


def delete_from_database(book_id: str) -> None:
    """
    A function used to delete a book from the database
    :param book_id: The id of the book to delete
    :return: None
    """

    # Making the sql command to delete the book
    command = (f"DELETE FROM {BOOKS_TABLE} "
               f"WHERE id = {book_id};")

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute(command)

    # Save and exit
    db.commit()
    cursor.close()
    db.close()


def add_author(unassigned_id: str = None) -> None:
    """
    This is used to get the data about an author.
    :param unassigned_id: This is to find inconsistencies with the data
    :return: None
    """

    # Loading the authors data and making sure there is data to load
    data = load_authors()
    if data:
        data = [x[0] for x in data]

    # Getting the ID for the author if one wasn't provided
    if unassigned_id:
        print(f"{unassigned_id} is the Author ID.")
        user_input = unassigned_id
    else:
        while True:
            user_input = get_id("What is the authors ID.\n")
            if data:
                if user_input in data:
                    print("Error that ID is already used.")
                else:
                    break
            else:
                break

    # Getting the rest of the information
    author_id = user_input
    author_name = get_information("What is the authors name?\n")
    author_country = get_information("What is the authors country?\n")

    # Putting all the data in a list and appending the authors database
    new_author = [author_id, author_name, author_country]
    append_authors(new_author)


def append_authors(data: list) -> None:
    """
    Used to write to the authors table.
    :param data: The data that is to be written to the table
    :return: None
    """

    # Making the connection
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # Making the command and putting it in the table
    command = (f"INSERT INTO {AUTHORS_TABLE}(id, name, country) "
               f"VALUES{tuple(data)};")
    cursor.execute(command)

    # Saving and closing the connection
    db.commit()
    cursor.close()
    db.close()


def get_information(question: str) -> str:
    """
    Used to get unverifiable data that the user has to confirm
    :param question: The question to be asked to the user
    :return: String that hopefully holds the desired information
    """

    # The user will remain in this look until they confirm that the
    # data is accurate.
    while True:
        user_input = input(question)
        if yes_or_no(f"Is ({user_input}) Correct?"):
            break

    return user_input


def add_missing_authors() -> None:
    """
    This takes the data from the books table and makes sure that
    the authors table has a match author and if not it prompts
    the user to insert the missing data.
    :return: Nothing
    """

    # Getting the data from the tables
    books_data = load_books()
    authors_data = load_authors()

    # Making sure there are books to check the author id of
    if not books_data:
        print("There are no books in the store.")
    else:

        # Getting all the id's of the current authors
        # to see what's missing.
        if not authors_data:
            authors_ids = []
        else:
            authors_ids = [x[0] for x in authors_data]
        books_authors_ids = [x[2] for x in books_data]

        # Finding the id's without author table information
        details_required = []
        for potentially_unused_id in books_authors_ids:
            if potentially_unused_id not in authors_ids:
                details_required.append(potentially_unused_id)

        # Displaying errors as needed or getting the missing information.
        if len(details_required) == 0:
            print("No authors need extra information.")
        else:
            for unused_id in details_required:
                add_author(unused_id)
            print("That's all the authors from the store.")


def view_authors() -> None:
    """
    This is used to view only the information of the authors and
    shows all the data
    :return: None
    """

    # Loading the data and making sure there is data to show.
    data = load_authors()
    if data:
        data = format_author_data(data)
        for line in data:
            print(line)
    else:
        print("No Authors to show.")


def format_author_data(data: list) -> list:
    """
    Takes in a list of authors and formats them all into a list of strings
    used to display the information.
    :param data: A list of author data lists NB
    :return: None
    """

    # Titles for the information about to be displayed
    titles = [
        "Author ID",
        "Name",
        "Country",
    ]

    # Formatting the data to be uniform and look good
    output = []
    counter = 0
    for author in data:
        counter += 1
        output.append(f"Author: {counter}")
        for i in range(3):
            string = f"{titles[i].ljust(10)}: {author[i]}"
            output.append(string)
        output.append("")

    return output


def update_author(data: list) -> None:
    """
    Used to update an existing entry in the author table
    :param data: new data to be changed
    :return: Nothing
    """

    # Connecting to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # Changing the data
    command = (f"UPDATE {AUTHORS_TABLE} "
               f"SET name = {data[1]}, country = {data[2]} "
               f"WHERE id = {data[0]};")
    cursor.execute(command)

    # Save and exit.
    db.commit()
    cursor.close()
    db.close()


# TODO to be added into a menu


def edit_author() -> None:
    """
    This is used to get the information to edit an author
    calls an updater to update the author table
    :return: None
    """

    # loads the data and makes sure there is information to edit.
    data = load_authors()
    if data:

        # Shows the user a list of authors to edit
        view_authors()
        index = get_digit(len(data), "type in the number of the "
                                     "author you want to edit.")
        author_to_edit = data[index-1]
        author_id, author_name, author_country = author_to_edit

        # The ID will remain unchanged.
        print(f"Authors ID is {author_id}")

        # Other information is gathered
        if yes_or_no(f"Do you want to change the name ({author_name})?"):
            author_name = get_information("What should the name of the author be?\n")

        if yes_or_no(f"Do you want to change the country ({author_country})?"):
            author_country = get_information("What should the authors country be?\n")

        # Data is compounded and updated in the table.
        new_author_data = [author_id, author_name, author_country]
        update_author(new_author_data)

    else:
        print("There are no authors to edit.")


def delete_author_selector() -> None:
    """
    Used to get the index of the author to delete
    Uses a different function to delete the author from the table
    :return: None
    """

    # Getting the data and then making sure there is data to act on
    data = load_authors()
    if data:
        view_authors()

        # Getting the data required to act on
        index = get_digit(len(data), "Which author would you like to delete?\n")
        author_to_delete = data[index-1]
        author_id_to_delete = author_to_delete[0]

        # Deleting it from the table
        delete_author(author_id_to_delete)
        print(f"Author {author_to_delete[1]} deleted")
    else:
        print("No authors to delete.")


def delete_author(author_id: str) -> None:
    """
    Used to delete an author from the table with the authors id
    :param author_id: the id of the author to be deleted
    :return: None
    """

    # Connect to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # Delete the required data
    command = (f"DELETE FROM {AUTHORS_TABLE} "
               f"WHERE id = {author_id};")
    cursor.execute(command)

    # Save and exit
    db.commit()
    cursor.close()
    db.close()


def view_all() -> None:
    """
    Used to view all information as detailed as possible.
    :return: None
    """

    # Getting all the data needed
    books_data = load_books()
    authors_data = load_authors()

    detailed_data = []

    # Collecting data
    # Checking if there are books
    if books_data:
        for book in books_data:
            author_name = author_country = "Not available."

            # Making sure there are authors and if there are finding
            # the right one and adding the data
            if authors_data:
                book_author_id = book[2]
                for author in authors_data:
                    if author[0] == book_author_id:
                        author_name, author_country = author[1:]

            book_name = book[1]
            book_quantity = book[3]

            # Compiling all the data into one list.
            detailed_data.append([book_name, book_quantity, author_name, author_country])

        # Formating the data to be easy to read.
        detailed_data = format_detailed(detailed_data)

        # Printing all the data out.
        for line in detailed_data:
            print(line)
    else:
        print("No books to view")


def format_detailed(data: list) -> list:
    """
    Formatting the data into easy to read strings.
    And then returning that.
    :param data: A list of data to be formatted.
    :return: Nothing
    """

    titles = [
        "Book Title",
        "Amount",
        "Author Name",
        "From"
    ]

    output = []
    counter = 0

    # Matching the data with the related title for easy reading.
    for book in data:
        counter += 1
        output.append(f"Book {counter}")
        for i in range(4):
            string = f"{titles[i].ljust(12)}: {book[i]}"
            output.append(string)
        output.append("="*20)

    return output


def main_menu() -> str:
    """
    This is used to get specific strings for the menu
    :return: string
    """
    user_input = ''

    # Making a list of possible options that is easily editable
    options = [
        "View All",
        "Books",
        "Authors",
        "Exit",
    ]

    # Dynamically adding the number options
    numbers = range(len(options))
    numbers = [str(x+1) for x in numbers]

    # Printing out the current accepted options and
    # keeping the user trapped until one is selected
    while user_input not in options and user_input not in numbers:
        print("\nThis is the main menu")
        for i in range(len(options)):
            print(f"{i+1}. {options[i]}")
        user_input = input("Please choose one on the above.\n").title()

    return user_input


def books_menu() -> None:
    """
    This is a sub menu to make the main menu less cluttered.
    :return: None
    """

    while True:
        user_input = books_menu_selector()
        match user_input:
            case "View" | "1":
                view_all_books()
            case "Add" | "2":
                add_new_book()
            case "Update" | "3":
                update_books()
            case "Delete" | "4":
                delete_book()
            case "Search" | "5":
                search_books()
            case "Exit" | "6":
                print("Going back to main menu.")
                break


def books_menu_selector() -> str:
    """
    This is a selector for the books menu to make sure that a valid response is given.
    :return: string choice
    """

    options = [
        "View",
        "Add",
        "Update",
        "Delete",
        "Search",
        "Exit",
    ]

    length = range(len(options))
    numbers = [str(x+1) for x in length]

    user_input = 0

    # The user can either give the exact name or the number equivalent.
    while user_input not in options and user_input not in numbers:
        print("This is the Books Menu")
        for i in length:
            print(f"{i+1}. {options[i]}")

        user_input = input("Select one of the above.\n").title()

    return user_input


def author_menu() -> None:
    """
    This is the menu for the authors part of things.
    :return: None
    """
    while True:
        user_input = author_menu_selector()
        match user_input:
            case "Add" | "1":
                add_author()
            case "View" | "2":
                view_authors()
            case "Edit" | "3":
                edit_author()
            case "Delete" | "4":
                delete_author_selector()
            case "Add Missing" | "5":
                add_missing_authors()
            case "Exit" | "6":
                print("Going back to the main menu.")
                break


def author_menu_selector() -> str:
    """
    This is the selector for the authors menu

    :return: str choice
    """
    options = [
        "Add",
        "View",
        "Edit",
        "Delete",
        "Add Missing",
        "Exit",
    ]

    # Making a dynamic number the user can select so they
    # don't have to type much
    length = range(len(options))
    numbers = [str(x+1) for x in length]

    # Printing out the options and keeping the user locked in
    # until one is chosen
    user_input = ''
    while user_input not in options and user_input not in numbers:
        print("This is the Authors Menu")
        for i in length:
            print(f"{i+1}. {options[i]}")

        user_input = input("Select one of the above.\n").title()

    return user_input


check_databases()
while True:
    action = main_menu()
    match action:
        case "View All" | "1":
            view_all()
        case "Books" | "2":
            books_menu()
        case "Authors" | "3":
            author_menu()
        case "Exit" | "4":
            print("Have a nice day")
            break
