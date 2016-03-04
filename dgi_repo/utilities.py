"""
Utility functions.
"""

PID_SEPARATOR = ':'


def bootstrap():
    """
    Run code that should always be ran at the begining of the application run.
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
    if (pid_id.count(PID_SEPARATOR)):
        raise ValueError(
            "Too many '{}' in the id: {}.".format(PID_SEPARATOR, pid_id)
        )

    return '{}{}{}'.format(pid_namespace, PID_SEPARATOR, pid_id)
