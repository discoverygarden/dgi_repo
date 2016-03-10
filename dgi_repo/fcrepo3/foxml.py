"""
Functions to help with FOXML.
"""

from dgi_repo import utilities as utils
from dgi_repo.fcrepo3 import relations

FOXML_NAMESPACE = 'info:fedora/fedora-system:def/foxml#'
SCHEMA_NAMESPACE = 'http://www.w3.org/2001/XMLSchema-instance'
SCHEMA_LOCATION = ('info:fedora/fedora-system:def/foxml# '
                   'http://www.fedora.info/definitions/1/0/foxml1-1.xsd')


def generate_foxml(pid):
    """
    Generate FOXML from a PID as a SpooledTemporaryFile.
    """
    from lxml import etree

    foxml_file = utils.SpooledTemporaryFile()
    # Using a spooled temp file, double buffering will just eat memory.
    with etree.xmlfile(foxml_file, buffered=False, encoding="utf-8") as foxml:
        foxml.write_declaration(version='1.0')
        populate_foxml_etree(foxml, pid)
        return foxml_file
    return None


def populate_foxml_etree(foxml, pid):
    """
    Generate FOXML from a PID into an lxml etree.
    """
    from dgi_repo import utilities as utils

    pid_namespace, pid_id = utils.break_pid(pid)

    attributes = {
        'VERSION': '1.1',
        'PID': pid,
    }

    with foxml.element('{{{0}}}digitalObject'.format(FOXML_NAMESPACE),
                       **attributes):
        pass

    return foxml
