"""
Tests API functionality.
"""

import unittest
import datetime

from lxml import etree

from dgi_repo.fcrepo3 import object_resource
from dgi_repo.fcrepo3 import api


class GetObjectProfileTestCase(unittest.TestCase):
    """
    Tests the get object profile endpoint.
    """

    def test_value(self):
        """
        Test object profile values.
        """
        my_object_resource = object_resource.ObjectResource()
        xml = my_object_resource._get_object_profile(
            'boaty:mcboatface',
            'intertubes',
            ['do:thereisnotry'],
            datetime.datetime.now(),
            datetime.datetime.now(),
            'A',
            'dr who'
        )
        tree = etree.fromstring(xml)

        label_xpath = etree.ETXPath(
            '//{{{}}}objLabel/text()'.format(api.FEDORA_ACCESS_URI)
        )
        self.assertEqual(label_xpath(tree)[0], 'intertubes')

        state_xpath = etree.ETXPath(
            '//{{{}}}objState/text()'.format(api.FEDORA_ACCESS_URI)
        )
        self.assertEqual(state_xpath(tree)[0], 'A')

        pid_xpath = etree.ETXPath(
            '/{{{}}}objectProfile/@pid'.format(api.FEDORA_ACCESS_URI)
        )
        self.assertEqual(pid_xpath(tree)[0], 'boaty:mcboatface')

        model_xpath = etree.ETXPath(
            '//{{{}}}model/text()'.format(api.FEDORA_ACCESS_URI)
        )
        self.assertIn('do:thereisnotry', model_xpath(tree))

        owner_xpath = etree.ETXPath(
            '//{{{}}}objOwnerId/text()'.format(api.FEDORA_ACCESS_URI)
        )
        self.assertEqual(owner_xpath(tree)[0], 'dr who')

if __name__ == '__main__':
    unittest.main()
