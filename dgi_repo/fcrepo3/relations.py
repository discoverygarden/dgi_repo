"""
Relationship specific code.
"""

# RDF namespaces.
ISLANDORA_RELS_EXT_NAMESPACE = 'http://islandora.ca/ontology/relsext#'
ISLANDORA_RELS_INT_NAMESPACE = 'http://islandora.ca/ontology/relsint#'
FEDORA_RELS_EXT_NAMESPACE = 'info:fedora/fedora-system:def/relations-external#'
FEDORA_MODEL_NAMESPACE = 'info:fedora/fedora-system:def/model#'
FEDORA_VIEW_NAMESPACE = 'info:fedora/fedora-system:def/view#'
DC_NAMESPACE = 'http://purl.org/dc/elements/1.1/'

# RDF predicates.
IS_CONSTITUENT_OF_PREDICATE = 'isConstituentOf'
IS_MEMBER_OF_PREDICATE = 'isMemberOf'
IS_MEMBER_OF_COLLECTION_PREDICATE = 'isMemberOfCollection'
HAS_MODEL_PREDICATE = 'hasModel'
STATE_PREDICATE = 'state'
LABEL_PREDICATE = 'label'
OWNER_PREDICATE = 'ownerId'
CREATED_DATE_PREDICATE = 'createdDate'
LAST_MODIFIED_DATE_PREDICATE = 'lastModifiedDate'
DEFER_DERIVATIVES_PREDICATE = 'deferDerivatives'
DATE_ISSUED_PREDICATE = 'dateIssued'
CONTRIBUTOR_PREDICATE = 'contributor'
COVERAGE_PREDICATE = 'coverage'
CREATOR_PREDICATE = 'creator'
DATE_PREDICATE = 'date'
DESCRIPTION_PREDICATE = 'description'
FORMAT_PREDICATE = 'format'
IDENTIFIER_PREDICATE = 'identifier'
LANGUAGE_PREDICATE = 'language'
PUBLISHER_PREDICATE = 'publisher'
RELATION_PREDICATE = 'relation'
RIGHTS_PREDICATE = 'rights'
SOURCE_PREDICATE = 'source'
SUBJECT_PREDICATE = 'subject'
TITLE_PREDICATE = 'title'
TYPE_PREDICATE = 'type'
GENERATE_OCR_PREDICATE = 'generate_ocr'
HAS_LANGUAGE_PREDICATE = 'has_language'
IMAGE_HEIGHT_PREDICATE = 'height'
IMAGE_WIDTH_PREDICATE = 'width'
IS_PAGE_OF_PREDICATE = 'isPageOf'
IS_PAGE_NUMBER_PREDICATE = 'isPageNumber'
IS_SECTION_PREDICATE = 'isSection'
IS_SEQUENCE_NUMBER_PREDICATE = 'isSequenceNumber'
DEFER_DERIVITIVES_PREDICATE = 'deferDerivatives'
IS_MANAGEABLE_BY_ROLE_PREDICATE = 'isManageableByRole'
IS_MANAGEABLE_BY_USER_PREDICATE = 'isManageableByUser'
IS_VIEWABLE_BY_ROLE_PREDICATE = 'isViewableByRole'
IS_VIEWABLE_BY_USER_PREDICATE = 'isViewableByUser'

# Predicate to namespace map.
RELATIONS = {
    ISLANDORA_RELS_EXT_NAMESPACE: [
        DATE_ISSUED_PREDICATE,
        DEFER_DERIVATIVES_PREDICATE,
        GENERATE_OCR_PREDICATE,
        HAS_LANGUAGE_PREDICATE,
        IS_PAGE_OF_PREDICATE,
        IS_PAGE_NUMBER_PREDICATE,
        IS_SECTION_PREDICATE,
        IS_SEQUENCE_NUMBER_PREDICATE,
        DEFER_DERIVATIVES_PREDICATE,
        IS_MANAGEABLE_BY_ROLE_PREDICATE,
        IS_MANAGEABLE_BY_USER_PREDICATE,
        IS_VIEWABLE_BY_ROLE_PREDICATE,
        IS_VIEWABLE_BY_USER_PREDICATE,
        IMAGE_HEIGHT_PREDICATE,
        IMAGE_WIDTH_PREDICATE,
    ],
    ISLANDORA_RELS_INT_NAMESPACE: [
        IS_MANAGEABLE_BY_ROLE_PREDICATE,
        IS_MANAGEABLE_BY_USER_PREDICATE,
        IS_VIEWABLE_BY_ROLE_PREDICATE,
        IS_VIEWABLE_BY_USER_PREDICATE,
    ],
    FEDORA_RELS_EXT_NAMESPACE: [
        IS_MEMBER_OF_COLLECTION_PREDICATE,
        IS_CONSTITUENT_OF_PREDICATE,
        IS_MEMBER_OF_PREDICATE,
    ],
    FEDORA_MODEL_NAMESPACE: [
        STATE_PREDICATE,
        LABEL_PREDICATE,
        OWNER_PREDICATE,
        CREATED_DATE_PREDICATE,
        HAS_MODEL_PREDICATE,
    ],
    FEDORA_VIEW_NAMESPACE: [
        LAST_MODIFIED_DATE_PREDICATE,
    ],
    DC_NAMESPACE: [
        CONTRIBUTOR_PREDICATE,
        COVERAGE_PREDICATE,
        CREATOR_PREDICATE,
        DATE_PREDICATE,
        DESCRIPTION_PREDICATE,
        FORMAT_PREDICATE,
        IDENTIFIER_PREDICATE,
        LANGUAGE_PREDICATE,
        PUBLISHER_PREDICATE,
        RELATION_PREDICATE,
        RIGHTS_PREDICATE,
        SOURCE_PREDICATE,
        SUBJECT_PREDICATE,
        TITLE_PREDICATE,
        TYPE_PREDICATE,
    ],
}
