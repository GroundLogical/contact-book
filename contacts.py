"""contacts.py - A Python module to save contact details.

This module uses a SQLite database to save contact details including name,
address, phone number and email address. Users can then access saved contact
details via the command line. The module also allows users to update existing
contact information, delete contacts and list saved contacts.

Usage Instructions
Add contact    > python contacts.py add
Edit contact   > python contacts.py edit <contact_id>
Delete contact > python contacts.py del <contact_id>
Find contact   > python contacts.py find <name>
List contacts  > python contacts.py list
"""

from pathlib import Path
import sqlite3
import sys

# Module constants.
COMMANDS = ('add', 'edit', 'del', 'find', 'list')
COLUMNS = {'1': 'name', '2': 'address', '3': 'phone', '4': 'email'}


def create_database():
    """Creates a new table in a SQLite database."""
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE contacts (
        contact_id INTEGER PRIMARY KEY,
        name TEXT,
        address TEXT,
        phone TEXT,
        email TEXT)'''
        )
    conn.commit()
    conn.close()


def add_contact():
    """Inserts a new contact into the database."""
    contact_details = get_contact_details()
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('INSERT INTO contacts (name, address, phone, email) '
              'VALUES (?, ?, ?, ?)', contact_details)
    conn.commit()
    conn.close()
    print(contact_details[0], 'added to contacts.')


def get_contact_details():
    """Prompts the user to input the new contact's details.

    Returns a tuple of the contacts name, address, phone and email address.
    """

    contact_details = []

    print("Input the new contact's details. Press Enter to continue.")
    name = input('Name:\n> ')
    address = input('Address:\n> ')
    phone = input('Phone number:\n> ')
    email = input('Email address:\n> ')

    contact_details.append(name.strip())
    contact_details.append(address.strip())
    contact_details.append(phone.strip())
    contact_details.append(email.strip())

    # The list of contact details must be converted to a tuple to be used by
    # the cursor object's execute method.
    return tuple(contact_details)


def edit_contact(contact_id):
    """Updates an existing contact's details in the database."""
    # Ensure the contact id is valid before attempting to edit the contact.
    if is_valid_id(contact_id):
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()

        # While loop so that more than one field can be edited in a session.
        while True:
            print('Input the number of the field you wish to edit and press '
                  'Enter. Leave blank to quit.\n'
                  '1 - Name\n'
                  '2 - Address\n'
                  '3 - Phone Number\n'
                  '4 - Email Address')

            field = input('> ')

            # If the response is left blank, break out of the while loop
            # without making any changes.
            if field.strip() == '':
                break

            # Ask the user again if the response is not in the desired format.
            elif field.strip() not in COLUMNS:
                print('Unrecognized command. Please try again.\n')
                continue

            # Prompt the user to enter the new value for the selected field.
            new_value = input('Enter the new value:\n> ')

            # Using string interpolation to dynamically set the column to be
            # updated since the execute method does not support
            # parameterization of column names.
            c.execute('UPDATE contacts SET %s=? WHERE contact_id=?'
                      % COLUMNS[field], (new_value, int(contact_id)))
            conn.commit()
            print('Update successful.\n')

        conn.close()


def delete_contact(contact_id):
    """Removes a contact from the database."""
    # Ensure the contact id is valid before attempting to delete the contact.
    if is_valid_id(contact_id):
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute('DELETE FROM contacts WHERE contact_id=?',
                  (int(contact_id),))
        conn.commit()
        conn.close()
        print('Contact deleted.')


def is_valid_id(contact_id):
    """Validates the user supplied contact id.

    Function ensures that the contact id is supplied in the correct format and
    that it exists in the database.

    Returns True or False.
    """

    # Check that the contact id is provided in numeric form.
    if not contact_id.isdecimal():
        print('Please use numeric characters for the Contact ID.')
        return False

    # Retrieve existing contact id's and ensure the user supplied id number is
    # in the database.
    contact_ids = get_contact_ids()
    if (int(contact_id),) not in contact_ids:
        print("No contacts found with that ID.\nCheck that you have specified "
              "the correct Contact ID. Use the find command to view a "
              "contact's ID number.")
        return False

    else:
        # The contact id is in the correct format and exists in the database.
        return True


def get_contact_ids():
    """Selects the id numbers of all contacts in the database.

    Returns a list of tuples containing the id numbers.
    """

    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    return c.execute('SELECT contact_id FROM contacts').fetchall()


def find_contact(name):
    """Selects existing contact details based on the provided name."""
    # Uses the LIKE operator to perform case insensitive searching. Also allows
    # for the use of the % and _ wildcards.
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('SELECT contact_id, name, address, phone, email '
              'FROM contacts WHERE name LIKE ?', (name,))
    results = c.fetchall()
    conn.close()
    display_contact_details(results)


def display_contact_details(results):
    """Displays an existing contact's details in the console."""
    print(f'{len(results)} result(s) found:')
    for result in results:
        print(f'''
Name:          {result[1]}
Address:       {result[2]}
Phone Number:  {result[3]}
Email Address: {result[4]}
Contact ID:    {result[0]}''')


def list_contacts():
    """Lists the names of contacts saved in the database."""
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    print('Contact List:')
    for row in c.execute('SELECT name FROM contacts'):
        print(row[0])
    conn.close()


def print_instructions():
    """Displays the module's usage instructions in the console."""
    print('''Usage Instructions
Add contact    > python contacts.py add
Edit contact   > python contacts.py edit <contact_id>
Delete contact > python contacts.py del <contact_id>
Find contact   > python contacts.py find <name>
List contacts  > python contacts.py list''')


def main():
    """Parses the command line arguments and calls the appropriate function."""
    if not Path('contacts.db').exists():
        create_database()

    if len(sys.argv) < 2 or sys.argv[1].lower() not in COMMANDS:
        print_instructions()

    elif sys.argv[1].lower() == 'add':
        add_contact()

    elif sys.argv[1].lower() == 'edit':
        try:
            edit_contact(sys.argv[2])
        except IndexError:
            # Handles exceptions caused when the user inputs edit but does
            # not specify a contact id.
            print('The edit command requires you to specify a Contact ID.\n'
                  'To view the usage instructions, run the program with no '
                  'commands.')

    elif sys.argv[1].lower() == 'del':
        try:
            delete_contact(sys.argv[2])
        except IndexError:
            # Handles exceptions caused when the user inputs del but does
            # not specify a contact id.
            print('The del command requires you to specify a Contact ID.\n'
                  'To view the usage instructions, run the program with no '
                  'commands.')

    elif sys.argv[1].lower() == 'find':
        find_contact(' '.join(sys.argv[2:]))

    elif sys.argv[1].lower() == 'list':
        list_contacts()


if __name__ == '__main__':
    main()
