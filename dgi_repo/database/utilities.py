"""
Database utility functions.
"""

import logging

import dgi_repo.fcrepo3.relations as rels

logger = logging.getLogger(__name__)

RELATION_MAP = {
    (rels.FEDORA_RELS_EXT_NAMESPACE, rels.IS_MEMBER_OF_COLLECTION_PREDICATE): (
        'is_member_of_collection',
        'Added an is member of collection relation from %s to %s.',
    ),
    (rels.FEDORA_RELS_EXT_NAMESPACE, rels.IS_MEMBER_OF_PREDICATE): (
        'is_member_of',
        'Added an "is member of" relation from %s to %s.',
    ),
    (rels.FEDORA_RELS_EXT_NAMESPACE, rels.IS_CONSTITUENT_OF_PREDICATE): (
        'is_constituent_of',
        'Added an "is constituent of" relation from %s to %s.',
    ),
    (rels.FEDORA_MODEL_NAMESPACE, rels.HAS_MODEL_PREDICATE): (
        'has_model',
        'Added content model to %s of %s.'
    ),
    (rels.DC_NAMESPACE, rels.CONTRIBUTOR_PREDICATE): (
        'dc_contributor',
        'Added a DC contributor relation about %s as %s.'
    ),
    (rels.DC_NAMESPACE, rels.COVERAGE_PREDICATE): (
        'dc_coverage',
        'Added a DC coverage relation about %s as %s.'
    ),
    (rels.DC_NAMESPACE, rels.CREATOR_PREDICATE): (
        'dc_creator',
        'Added a DC creator relation about %s as %s.'
    ),
    (rels.DC_NAMESPACE, rels.DATE_PREDICATE): (
        'dc_date',
        'Added a DC date relation about %s as %s.'
    ),
    (rels.DC_NAMESPACE, rels.DESCRIPTION_PREDICATE): (
        'dc_description',
        'Added a DC description relation about %s as %s.'
    ),
    (rels.DC_NAMESPACE, rels.FORMAT_PREDICATE): (
        'dc_format',
        'Added a DC format relation about %s as %s.'
    ),
    (rels.DC_NAMESPACE, rels.IDENTIFIER_PREDICATE): (
        'dc_identifier',
        'Added a DC identifier relation about %s as %s.'
    ),
    (rels.DC_NAMESPACE, rels.LANGUAGE_PREDICATE): (
        'dc_language',
        'Added a DC language relation about %s as %s.'
    ),
    (rels.DC_NAMESPACE, rels.PUBLISHER_PREDICATE): (
        'dc_publisher',
        'Added a DC publisher relation about %s as %s.'
    ),
    (rels.DC_NAMESPACE, rels.RELATION_PREDICATE): (
        'dc_relation',
        'Added a DC relation relation about %s as %s.'
    ),
    (rels.DC_NAMESPACE, rels.RIGHTS_PREDICATE): (
        'dc_rights',
        'Added a DC rights relation about %s as %s.'
    ),
    (rels.DC_NAMESPACE, rels.SOURCE_PREDICATE): (
        'dc_source',
        'Added a DC source relation about %s as %s.'
    ),
    (rels.DC_NAMESPACE, rels.SUBJECT_PREDICATE): (
        'dc_subject',
        'Added a DC subject relation about %s as %s.'
    ),
    (rels.DC_NAMESPACE, rels.TITLE_PREDICATE): (
        'dc_title',
        'Added a DC title relation about %s as %s.'
    ),
    (rels.DC_NAMESPACE, rels.TYPE_PREDICATE): (
        'dc_type',
        'Added a DC type relation about %s as %s.'
    ),
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.DATE_ISSUED_PREDICATE): (
        'date_issued',
        'Added a date issued relation about %s as %s.'
    ),
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.GENERATE_OCR_PREDICATE): (
        'generate_ocr',
        'Added a generate OCR relation about %s as %s.'
    ),
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.HAS_LANGUAGE_PREDICATE): (
        'has_language',
        'Added a languge relation about %s as %s.'
    ),
    (rels.ISLANDORA_RELS_INT_NAMESPACE, rels.IMAGE_HEIGHT_PREDICATE): (
        'image_height',
        'Added a height cache relation about %s as %s.'
    ),
    (rels.ISLANDORA_RELS_INT_NAMESPACE, rels.IMAGE_WIDTH_PREDICATE): (
        'image_width',
        'Added a width cache relation about %s as %s.'
    ),
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_PAGE_NUMBER_PREDICATE): (
        'is_page_number',
        'Added a page number relation about %s as %s.'
    ),
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_PAGE_OF_PREDICATE): (
        'is_page_of',
        'Added a page of relation about %s to %s.'
    ),
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_SECTION_PREDICATE): (
        'is_section',
        'Added a section relation about %s as %s.'
    ),
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_SEQUENCE_NUMBER_PREDICATE): (
        'is_sequence_number',
        'Added a sequence number relation about %s as %s.'
    ),
}

DATASTREAM_RELATION_MAP = RELATION_MAP.copy()
DATASTREAM_RELATION_MAP.update({
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_MANAGEABLE_BY_ROLE_PREDICATE): (
        'datastream_is_manageable_by_role',
        'Added a datastream is manageable by role permission from %s to %s.'
    ),
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_MANAGEABLE_BY_USER_PREDICATE): (
        'datastream_is_manageable_by_user',
        'Added a datastream is manageable by user permission from %s to %s.'
    ),
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_VIEWABLE_BY_ROLE_PREDICATE): (
        'datastream_is_viewable_by_role',
        'Added a datastream is viewable by role permission from %s to %s.'
    ),
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_VIEWABLE_BY_USER_PREDICATE): (
        'datastream_is_viewable_by_user',
        'Added a datastream is viewable by user permission from %s to %s.'
    ),
})

OBJECT_RELATION_MAP = RELATION_MAP.copy()
OBJECT_RELATION_MAP.update({
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_MANAGEABLE_BY_ROLE_PREDICATE): (
        'object_is_manageable_by_role',
        'Added an object is manageable by role permission from %s to %s.'
    ),
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_MANAGEABLE_BY_USER_PREDICATE): (
        'object_is_manageable_by_user',
        'Added an object is manageable by user permission from %s to %s.'
    ),
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_VIEWABLE_BY_ROLE_PREDICATE): (
        'object_is_viewable_by_role',
        'Added an object is viewable by role permission from %s to %s.'
    ),
    (rels.ISLANDORA_RELS_EXT_NAMESPACE, rels.IS_VIEWABLE_BY_USER_PREDICATE): (
        'object_is_viewable_by_user',
        'Added an object is viewable by user permission from %s to %s.'
    ),
})


def get_connection():
    """
    Get a connection to the application database.
    """

    from psycopg2 import connect

    from dgi_repo.configuration import configuration

    connection_string = 'dbname={} user={} password={} host={}'.format(
        configuration['database']['name'],
        configuration['database']['username'],
        configuration['database']['password'],
        configuration['database']['host']
    )

    return connect(connection_string)


def check_cursor(cursor=None):
    """
    Check if a cursor is valid, receiving it or a valid one.
    """
    if cursor is None:
        db_connection = get_connection()
        db_connection.autocommit = True
        return db_connection.cursor()
    else:
        return cursor


def install_schema():
    """
    Install the application schema to the database.
    """

    from os.path import join, dirname
    db_connection = get_connection()
    with db_connection:
        with open(join(dirname(__file__), 'resources', 'dgi_repo.sql'), 'r') as schema_file:
            with db_connection.cursor() as db_cursor:
                db_cursor.execute(schema_file.read())
    db_connection.close()
    logger.info('Installed schema.')


def install_base_data():
    """
    Install the application's base data to the database.
    """

    import dgi_repo.database.write.relations as relations_writer
    from dgi_repo.fcrepo3.relations import RELATIONS as rels

    db_connection = get_connection()
    with db_connection:
        with db_connection.cursor() as cursor:
            for namespace, predicates in rels.items():

                relations_writer.upsert_namespace(namespace, cursor)
                namespace_id = cursor.fetchone()

                for predicate in predicates:
                    relations_writer.upsert_predicate(
                        {'namespace':namespace_id, 'predicate':predicate},
                        cursor
                    )

    db_connection.close()
    logger.info('Installed base data.')
