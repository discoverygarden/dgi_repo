"""
Database utility functions.
"""
from psycopg2 import connect
from psycopg2.extras import DictCursor
from psycopg2.extensions import ISOLATION_LEVEL_REPEATABLE_READ

from dgi_repo.configuration import configuration as _config
import dgi_repo.fcrepo3.relations as rels

DATASTREAM_RELATION_MAP = {
    (rels.ISLANDORA_RELS_INT_NAMESPACE, rels.IMAGE_HEIGHT_PREDICATE): {
        'table': 'image_height',
        'upsert message': 'Added a height cache relation about %s as %s.',
        'delete message': 'Deleted a height cache relation with ID: %s.',
    },
    (rels.ISLANDORA_RELS_INT_NAMESPACE, rels.IMAGE_WIDTH_PREDICATE): {
        'table': 'image_width',
        'upsert message': 'Added a width cache relation about %s as %s.',
        'delete message': 'Deleted a width cache relation with ID: %s.',
    },
    (rels.ISLANDORA_RELS_INT_NAMESPACE,
     rels.IS_MANAGEABLE_BY_ROLE_PREDICATE): {
        'table': 'datastream_is_manageable_by_role',
        'upsert message': ('Added a datastream is manageable by role'
                           ' permission from %s to %s.'),
        'delete message': ('Deleted a datastream is manageable by role'
                           ' permission with ID: %s.'),
    },
    (rels.ISLANDORA_RELS_INT_NAMESPACE,
     rels.IS_MANAGEABLE_BY_USER_PREDICATE): {
        'table': 'datastream_is_manageable_by_user',
        'upsert message': ('Added a datastream is manageable by user'
                           ' permission from %s to %s.'),
        'delete message': ('Deleted a datastream is manageable by user'
                           ' permission with ID: %s.'),
    },
    (rels.ISLANDORA_RELS_INT_NAMESPACE, rels.IS_VIEWABLE_BY_ROLE_PREDICATE): {
        'table': 'datastream_is_viewable_by_role',
        'upsert message': ('Added a datastream is viewable by role permission'
                           ' from %s to %s.'),
        'delete message': ('Deleted a datastream is viewable by role'
                           ' permission with ID: %s.'),
    },
    (rels.ISLANDORA_RELS_INT_NAMESPACE, rels.IS_VIEWABLE_BY_USER_PREDICATE): {
        'table': 'datastream_is_viewable_by_user',
        'upsert message': ('Added a datastream is viewable by user permission'
                           ' from %s to %s.'),
        'delete message': ('Deleted a datastream is viewable by user'
                           ' permission with ID: %s.'),
    },
}

OBJECT_RELATION_MAP = {
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_PAGE_NUMBER_PREDICATE): {
        'table': 'is_page_number',
        'upsert message': 'Added a page number relation about %s as %s.',
        'delete message': 'Deleted a page number relation with ID: %s.',
    },
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_PAGE_OF_PREDICATE): {
        'table': 'is_page_of',
        'upsert message': 'Added a page of relation about %s to %s.',
        'delete message': 'Deleted a page of relation with ID: %s.',
    },
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_SECTION_PREDICATE): {
        'table': 'is_section',
        'upsert message': 'Added a section relation about %s as %s.',
        'delete message': 'Deleted a section relation with ID: %s.',
    },
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_SEQUENCE_NUMBER_PREDICATE): {
        'table': 'is_sequence_number',
        'upsert message': 'Added a sequence number relation about %s as %s.',
        'delete message': 'Deleted a sequence number relation with ID: %s.',
    },
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.DEFER_DERIVATIVES_PREDICATE): {
        'table': 'defer_derivatives',
        'upsert message': 'Added a defer derivatives relation about %s as %s.',
        'delete message': 'Deleted a defer derivatives relation with ID: %s.',
    },
    (rels.FEDORA_RELS_EXT_NAMESPACE, rels.IS_MEMBER_OF_COLLECTION_PREDICATE): {
        'table': 'is_member_of_collection',
        'upsert message': ('Added an "is member of collection" relation from'
                           ' %s to %s.'),
        'delete message': ('Deleted an "is member of collection" relation with'
                           ' ID: %s.'),
    },
    (rels.FEDORA_RELS_EXT_NAMESPACE, rels.IS_MEMBER_OF_PREDICATE): {
        'table': 'is_member_of',
        'upsert message': 'Added an "is member of" relation from %s to %s.',
        'delete message': 'Deleted an "is member of" relation with ID: %s.',
    },
    (rels.FEDORA_RELS_EXT_NAMESPACE, rels.IS_CONSTITUENT_OF_PREDICATE): {
        'table': 'is_constituent_of',
        'upsert message': ('Added an "is constituent of" relation from %s to'
                           ' %s.'),
        'delete message': ('Deleted an "is constituent of" relation with ID:'
                           ' %s.'),
    },
    (rels.FEDORA_MODEL_NAMESPACE, rels.HAS_MODEL_PREDICATE): {
        'table': 'has_model',
        'upsert message': 'Added content model to %s of %s.',
        'delete message': 'Deleted a content model relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.CONTRIBUTOR_PREDICATE): {
        'table': 'dc_contributor',
        'upsert message': 'Added a DC contributor relation about %s as %s.',
        'delete message': 'Deleted a DC contributor relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.COVERAGE_PREDICATE): {
        'table': 'dc_coverage',
        'upsert message': 'Added a DC coverage relation about %s as %s.',
        'delete message': 'Deleted a DC coverage relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.CREATOR_PREDICATE): {
        'table': 'dc_creator',
        'upsert message': 'Added a DC creator relation about %s as %s.',
        'delete message': 'Deleted a DC creator relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.DATE_PREDICATE): {
        'table': 'dc_date',
        'upsert message': 'Added a DC date relation about %s as %s.',
        'delete message': 'Deleted a DC date relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.DESCRIPTION_PREDICATE): {
        'table': 'dc_description',
        'upsert message': 'Added a DC description relation about %s as %s.',
        'delete message': 'Deleted a DC description relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.FORMAT_PREDICATE): {
        'table': 'dc_format',
        'upsert message': 'Added a DC format relation about %s as %s.',
        'delete message': 'Deleted a DC format relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.IDENTIFIER_PREDICATE): {
        'table': 'dc_identifier',
        'upsert message': 'Added a DC identifier relation about %s as %s.',
        'delete message': 'Deleted a DC identifier relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.LANGUAGE_PREDICATE): {
        'table': 'dc_language',
        'upsert message': 'Added a DC language relation about %s as %s.',
        'delete message': 'Deleted a DC language relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.PUBLISHER_PREDICATE): {
        'table': 'dc_publisher',
        'upsert message': 'Added a DC publisher relation about %s as %s.',
        'delete message': 'Deleted a DC publisher relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.RELATION_PREDICATE): {
        'table': 'dc_relation',
        'upsert message': 'Added a DC relation relation about %s as %s.',
        'delete message': 'Deleted a DC relation relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.RIGHTS_PREDICATE): {
        'table': 'dc_rights',
        'upsert message': 'Added a DC rights relation about %s as %s.',
        'delete message': 'Deleted a DC rights relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.SOURCE_PREDICATE): {
        'table': 'dc_source',
        'upsert message': 'Added a DC source relation about %s as %s.',
        'delete message': 'Deleted a DC source relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.SUBJECT_PREDICATE): {
        'table': 'dc_subject',
        'upsert message': 'Added a DC subject relation about %s as %s.',
        'delete message': 'Deleted a DC subject relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.TITLE_PREDICATE): {
        'table': 'dc_title',
        'upsert message': 'Added a DC title relation about %s as %s.',
        'delete message': 'Deleted a DC title relation with ID: %s.',
    },
    (rels.DC_NAMESPACE, rels.TYPE_PREDICATE): {
        'table': 'dc_type',
        'upsert message': 'Added a DC type relation about %s as %s.',
        'delete message': 'Deleted a DC type relation with ID: %s.',
    },
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.DATE_ISSUED_PREDICATE): {
        'table': 'date_issued',
        'upsert message': 'Added a date issued relation about %s as %s.',
        'delete message': 'Deleted a date issued relation with ID: %s.',
    },
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.GENERATE_OCR_PREDICATE): {
        'table': 'generate_ocr',
        'upsert message': 'Added a generate OCR relation about %s as %s.',
        'delete message': 'Deleted a generate OCR relation with ID: %s.',
    },
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.HAS_LANGUAGE_PREDICATE): {
        'table': 'has_language',
        'upsert message': 'Added a language relation about %s as %s.',
        'delete message': 'Deleted a language relation with ID: %s.',
    },
    (rels.ISLANDORA_RELS_EXT_NAMESPACE,
     rels.IS_MANAGEABLE_BY_ROLE_PREDICATE): {
        'table': 'object_is_manageable_by_role',
        'upsert message': ('Added an object is manageable by role permission'
                           ' from %s to %s.'),
        'delete message': ('Deleted an object is manageable by role permission'
                           ' with ID: %s.'),
    },
    (rels.ISLANDORA_RELS_EXT_NAMESPACE,
     rels.IS_MANAGEABLE_BY_USER_PREDICATE): {
        'table': 'object_is_manageable_by_user',
        'upsert message': ('Added an object is manageable by user permission'
                           ' from %s to %s.'),
        'delete message': ('Deleted an object is manageable by user'
                           ' permission with ID: %s.'),
    },
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_VIEWABLE_BY_ROLE_PREDICATE): {
        'table': 'object_is_viewable_by_role',
        'upsert message': ('Added an object is viewable by role permission'
                           ' from %s to %s.'),
        'delete message': ('Deleted an object is viewable by role permission'
                           ' with ID: %s.'),
    },
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_VIEWABLE_BY_USER_PREDICATE): {
        'table': 'object_is_viewable_by_user',
        'upsert message': ('Added an object is viewable by user permission'
                           ' from %s to %s.'),
        'delete message': ('Deleted an object is viewable by user permission'
                           ' with ID: %s.'),
    },
}

LITERAL_RDF_OBJECT = 'literal'
URI_RDF_OBJECT = 'uri'
RAW_RDF_OBJECT = 'raw'
OBJECT_RDF_OBJECT = 'object'
DATASTREAM_RDF_OBJECT = 'datastream'
USER_RDF_OBJECT = 'user'
ROLE_RDF_OBJECT = 'role'
LINKED_RDF_OBJECT_TYPES = set([OBJECT_RDF_OBJECT, DATASTREAM_RDF_OBJECT,
                               USER_RDF_OBJECT, ROLE_RDF_OBJECT])


def get_connection(isolation_level=ISOLATION_LEVEL_REPEATABLE_READ):
    """
    Get a connection to the application database.

    In general isolation level doesn't need to be changed unless you are
    stashing files, so as your transaction can be aware of them.
    """
    if isolation_level is None:
        isolation_level = ISOLATION_LEVEL_REPEATABLE_READ

    connection_string = 'dbname={} user={} password={} host={}'.format(
        _config['database']['name'],
        _config['database']['username'],
        _config['database']['password'],
        _config['database']['host']
    )

    connection = connect(connection_string, cursor_factory=DictCursor)

    connection.set_isolation_level(isolation_level)

    return connection


def check_cursor(cursor=None, isolation_level=None):
    """
    Check if a cursor is valid, receiving it or a valid one in autocommit mode.
    """
    if cursor is None:
        db_connection = get_connection(isolation_level)
        db_connection.autocommit = True
        return db_connection.cursor()
    else:
        return cursor
