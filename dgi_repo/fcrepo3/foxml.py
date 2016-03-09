"""
Functions to help with FOXML.
"""


def generate_foxml(pid):
    """
    Generate FOXML from a PID as a SpooledTemporaryFile.
    """
    from dgi_repo import utilities as utils

    pid_namespace, pid_id = utils.break_pid(pid)
    foxml_file = utils.SpooledTemporaryFile()

    return foxml_file
