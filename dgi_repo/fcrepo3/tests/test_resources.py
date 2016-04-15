"""
Tests resources functionality.
"""

import unittest
import unittest.mock
from unittest.mock import MagicMock

from dgi_repo.fcrepo3 import resources
from dgi_repo.configuration import configuration as _configuration


class GetNextPidTestCase(unittest.TestCase):
    """
    Tests the get next PID endpoint.
    """

    @unittest.mock.patch(
        'dgi_repo.fcrepo3.resources.object_writer.get_pid_ids'
    )
    def test_single_pid_gen(self, mock_pids):
        """
        Test for correct single default NS PID.
        """
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {'highest_id': 5}
        mock_pids.return_value = mock_cursor

        pid_resource = resources.PidResource()
        new_pids = pid_resource._get_pids()

        self.assertEqual(
            new_pids,
            ['{}:5'.format(_configuration['default_namespace'])]
        )

if __name__ == '__main__':
    unittest.main()
