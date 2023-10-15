"""
Custom Django command tests
"""
from unittest.mock import patch
from psycopg2 import OperationalError as PC2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db(self, patched_check):
        """Wait for database until is open for connection"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_with_delay(self, patched_sleep, patched_check):
        """Wait for database with long connection until is open for connection"""
        patched_check.side_effect = [PC2Error] * 2 + [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
