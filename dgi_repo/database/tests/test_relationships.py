"""
Tests relationship resolution functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
from lxml import etree

import dgi_repo.fcrepo3.relations as relations
from dgi_repo.fcrepo3.utilities import RDF_NAMESPACE
from dgi_repo.database.utilities import (LITERAL_RDF_OBJECT, URI_RDF_OBJECT,
                                         USER_RDF_OBJECT, ROLE_RDF_OBJECT,
                                         OBJECT_RDF_OBJECT,
                                         DATASTREAM_RDF_OBJECT)
from dgi_repo.database import relationships


class DatabaseRelationshipTestCase(unittest.TestCase):
    """
    Tests relationship parsing.
    """

    def setUp(self):
        self.namespace = 'http://example.org'
        self.name = 'example'
        self.element = etree.Element('{{{}}}{}'.format(self.namespace,
                                                       self.name))
        self.pred_map = dict()

    def test_parse_tuple(self):
        self.assertEqual(relationships._element_predicate(self.element),
                         (self.namespace, self.name))

    def test_text_predicate(self):
        text = "Some text"
        self.element.text = text

        self.assertEqual(self._map_lookup(), (text, LITERAL_RDF_OBJECT))

        with self.assertRaises(ValueError):
            self._base_lookup()

        self._add_to_map()
        with self.assertRaises(ValueError):
            self._map_lookup()

    @patch('dgi_repo.database.write.sources.upsert_user')
    def test_user_predicate(self, upsert_user):
        self.element.tag = '{{{}}}{}'.format(
            relations.ISLANDORA_RELS_INT_NAMESPACE,
            relations.IS_VIEWABLE_BY_USER_PREDICATE
        )
        self.element.text = 'Bob Loblaw'
        uid = 132
        upsert_user.return_value = self._get_mock_cursor_fetchone({
            'id': uid
        })
        self.assertEqual(self._base_lookup(), (uid, USER_RDF_OBJECT))
        upsert_user.assert_called_with({'name': self.element.text,
                                        'source': None}, cursor=None)

    @patch('dgi_repo.database.write.sources.upsert_role')
    def test_role_predicate(self, upsert_role):
        rid = 132
        upsert_role.return_value = self._get_mock_cursor_fetchone({
            'id': rid
        })
        self.element.tag = '{{{}}}{}'.format(
            relations.ISLANDORA_RELS_INT_NAMESPACE,
            relations.IS_VIEWABLE_BY_ROLE_PREDICATE
        )
        self.element.text = 'Those Guys'
        self.assertEqual(self._base_lookup(), (rid, ROLE_RDF_OBJECT))
        upsert_role.assert_called_with({'role': self.element.text,
                                        'source': None}, cursor=None)

    def _patch_object_info_from_raw(self, object_info_from_raw, object_id=42):
        object_info_from_raw.return_value = self._get_mock_cursor_fetchone({
            'id': object_id
        })

    def _get_mock_cursor_fetchone(self, data):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = data
        return mock_cursor

    @patch('dgi_repo.database.read.repo_objects.object_info_from_raw')
    def test_object_predicate(self, object_info_from_raw):
        object_id = 8601
        self._patch_object_info_from_raw(object_info_from_raw, object_id)
        uri = 'info:fedora/that:object'
        self.element.set('{{{}}}resource'.format(RDF_NAMESPACE), uri)

        self.assertEqual(self._base_lookup(), (object_id, OBJECT_RDF_OBJECT))

    @patch('dgi_repo.database.read.repo_objects.object_info_from_raw')
    @patch('dgi_repo.database.read.datastreams.datastream_id')
    def test_datastream_predicate(self, datastream_id, object_info_from_raw):
        ds_db_id = 9001
        self._patch_object_info_from_raw(object_info_from_raw)
        datastream_id.return_value = self._get_mock_cursor_fetchone({
            'id': ds_db_id
        })

        uri = 'info:fedora/that:object/SOME_DATASTREAM_ID'
        self.element.set('{{{}}}resource'.format(RDF_NAMESPACE), uri)
        self.assertEqual(self._base_lookup(), (ds_db_id,
                                               DATASTREAM_RDF_OBJECT))

    def _add_to_map(self):
        """
        Helper; add the current element to the map.

        Future calls to self._map_lookup() should return the same result as
        self._base_lookup().
        """
        self.pred_map[relationships._element_predicate(self.element)] = True

    def _map_lookup(self):
        """
        Helper; attempt resolution using table mapping.
        """
        return relationships._require_mapped(self.element, self.pred_map, None,
                                             None)

    def _base_lookup(self):
        """
        Helper; attempt resolution.
        """
        return relationships._rdf_object_from_element(
            relationships._element_predicate(self.element),
            self.element, None, None)

    def test_uri_predicate(self):
        uri = 'some://uri'
        self.element.set('{{{}}}resource'.format(RDF_NAMESPACE), uri)
        self.assertEqual(self._map_lookup(), (uri, URI_RDF_OBJECT))

        with self.assertRaises(ValueError):
            relationships._rdf_object_from_element(
                relationships._element_predicate(self.element),
                self.element, None, None)

    def test_dereference_empty_element(self):
        with self.assertRaises(KeyError):
            self._base_lookup()

        with self.assertRaises(ValueError):
            self._map_lookup()

        self._add_to_map()
        with self.assertRaises(KeyError):
            self._map_lookup()

if __name__ == '__main__':
    unittest.main()
