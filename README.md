# Contact Book

A Python module to save contact details. The module uses a SQLite database to save contact details including name, address, phone number and email address. Users can then access saved contact details via the command line. The module also allows users to update existing contact information, delete contacts and list all saved contacts.

## Installation

Clone the repository.

```shell
> git clone https://github.com/GroundLogical/contact-book
```

Alternatively, you can use the green "Code" download button. Choose the "Download ZIP" option from the drop-down menu. The ZIP file will contain the entire repository content.

## Usage

The following instructions assume that you have the Python Interpreter installed on your machine and that it has been added to the PATH environment variable.

From the command line, navigate to the directory where the module is saved and enter one of the following commands.

### Add Contact

```shell
> python contacts.py add
```

You will then be prompted to input the new contact's details. When you have finished typing, press Enter to continue. You may leave any number of fields blank if you so choose. At this time, the program does not prevent the user from inputting contacts with the same phone number or email address. This feature may be added in the future.

### Find Contact

```shell
> python contacts.py find <name>
```

Depending on the name you enter, the results will look something like this.

```shell
1 result(s) found:

Name:          John Doe
Address:       Somewhere
Phone Number:  555-1234
Email Address: example@email.com
Contact ID:    7
```

Replace \<name> with the name of the contact you wish to search for. Note that the find command is case-insensitive and supports the use of _ and % wildcards to match a single character or zero or more characters, respectively.

### Edit Contact

```shell
> python contacts.py edit <contact_id>
```

You will then be prompted to select a field to edit and to input the new data. This process can be repeated for multiple fields. To exit the program, leave the input blank and press Enter. The \<contact_id> must be in numeric form. If you do not know the ID of the contact you wish to edit, use the find command first.

### Delete Contact

```shell
> python contacts.py del <contact_id>
```

Use caution when using the del command because the action takes place immediately and the changes are permanent. Again the \<contact_id> must be in numeric form. If you do not know the ID of the contact you wish to delete, use the find command first.

### List Contacts

```shell
> python contacts.py list
```

Lists the name of every contact saved in the database.

## Support

For help, please use the issue tracker at.

> https://github.com/GroundLogical/contact-book/issues

## Roadmap

No plans for future releases at this time.

## License

This software is provided under the MIT License. For complete details refer to LICENSE.txt.

## Project Status

I created this project to practice my Python skills. I am sharing this code in the off-chance it helps someone else who is also learning. At this time, I do not have plans to actively develop this project. However, constructive feedback is always welcome and appreciated.