"""Tests for contacts.py"""

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

# Add parent directory to sys.path so the contacts module can be imported.
current_dir = Path().resolve()
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

import contacts  # noqa: E402

# Test constants.
CONTACT_DETAILS = ('John Doe', 'Somewhere', '555-1234', 'example@email.com')


class TestContacts(unittest.TestCase):

    def test_create_database(self):
        contacts.create_database()
        self.assertTrue(Path('contacts.db').exists())

    @patch('contacts.get_contact_details')
    @patch('sqlite3.connect')
    def test_add_contact(self, mock_connection, mock_details):
        mock_details.return_value = CONTACT_DETAILS
        mock_conn = mock_connection.return_value
        mock_c = mock_conn.cursor.return_value
        contacts.add_contact()
        mock_c.execute.assert_called_once_with(
            'INSERT INTO contacts (name, address, phone, email) '
            'VALUES (?, ?, ?, ?)', CONTACT_DETAILS
            )

    @patch('contacts.input', side_effect=['1', 'Jane Doe', ''])
    @patch('contacts.is_valid_id')
    @patch('sqlite3.connect')
    def test_edit_contact(self, mock_connection, mock_id, mock_input):
        mock_id.return_value = True
        mock_conn = mock_connection.return_value
        mock_c = mock_conn.cursor.return_value
        contacts.edit_contact('1')
        mock_c.execute.assert_called_once_with(
            'UPDATE contacts SET name=? WHERE contact_id=?', ('Jane Doe', 1)
            )

    @patch('contacts.is_valid_id')
    @patch('sqlite3.connect')
    def test_delete_contact(self, mock_connection, mock_id):
        mock_id.return_value = True
        mock_conn = mock_connection.return_value
        mock_c = mock_conn.cursor.return_value
        contacts.delete_contact('1')
        mock_c.execute.assert_called_once_with(
            'DELETE FROM contacts WHERE contact_id=?', (1,)
            )

    @patch('sqlite3.connect')
    def test_find_contact(self, mock_connection):
        mock_conn = mock_connection.return_value
        mock_c = mock_conn.cursor.return_value
        contacts.find_contact('John Doe')
        mock_c.execute.assert_called_once_with(
            'SELECT contact_id, name, address, phone, email '
            'FROM contacts WHERE name LIKE ?', ('John Doe',)
            )

    @classmethod
    def tearDownClass(cls):
        Path('contacts.db').unlink()


if __name__ == '__main__':
    unittest.main()
