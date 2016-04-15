"""
Tests FOXML functionality.
"""

import unittest

from dgi_repo.fcrepo3 import foxml


class FedoraUriTestCase(unittest.TestCase):
    """
    Tests Fedora URI parsing.
    """

    def test_is_uri(self):
        """
        Test for URI detection.
        """
        self.assertTrue(foxml.is_fedora_uri('info:fedora/bon_bon'))
        self.assertFalse(foxml.is_fedora_uri('Hamlet_A3S3L92'))

    def test_detect_pid(self):
        """
        Test for PID detection.
        """
        self.assertEqual(
            foxml.pid_from_fedora_uri('info:fedora/stuff:and_things'),
            'stuff:and_things'
        )
        self.assertEqual(
            foxml.pid_from_fedora_uri('info:fedora/stuff:and_things/items'),
            'stuff:and_things'
        )

    def test_dsid_detection(self):
        """
        Test for DSID detection.
        """
        self.assertEqual(
            foxml.dsid_from_fedora_uri(
                'info:fedora/stuff:and_things/items'
            ),
            'items'
        )

if __name__ == '__main__':
    unittest.main()
