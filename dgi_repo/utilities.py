"""
Utility functions.
"""

PID_SEPARATOR = ':'


def bootstrap():
    """
    Run code that should always be ran at the beginning of the application run.
    """

    import dgi_repo.logger

    dgi_repo.logger.configure_logging()


def install():
    """
    Run code to finish installing the application.
    """

    import dgi_repo.database.utilities as db_utils

    db_utils.install_schema()
    db_utils.install_base_data()


def break_pid(pid):
    """
    Break a PID into its constituent parts of namespace and ID.
    """
    if (pid.count(PID_SEPARATOR) > 1):
        raise ValueError(
            "Too many '{}' in PID: {}.".format(PID_SEPARATOR, pid)
        )
    if (pid.count(PID_SEPARATOR) < 1):
        raise ValueError("Too few '{}' in PID: {}.".format(PID_SEPARATOR, pid))

    return pid.split(PID_SEPARATOR)


def make_pid(pid_namespace, pid_id):
    """
    Join a namespace and ID into a PID.
    """
    if (pid_namespace.count(PID_SEPARATOR)):
        raise ValueError(
            "Too many '{}' in the namespace: {}.".format(
                PID_SEPARATOR,
                pid_namespace
            )
        )
    if (str(pid_id).count(PID_SEPARATOR)):
        raise ValueError(
            "Too many '{}' in the id: {}.".format(PID_SEPARATOR, pid_id)
        )

    return '{}{}{}'.format(pid_namespace, PID_SEPARATOR, pid_id)


def SpooledTemporaryFile(*args, **kwargs):
    """
    Call tempfile.SpooledTemporaryFile with configured defaults.
    """
    from tempfile import SpooledTemporaryFile

    from dgi_repo.configuration import configuration

    if args:
        spooled_file = SpooledTemporaryFile(*args, **kwargs)
    else:
        spooled_file = SpooledTemporaryFile(
            configuration['spooled_temp_file_size'],
            **kwargs
        )

    return spooled_file
