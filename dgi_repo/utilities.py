"""
Utility functions.
"""
from tempfile import SpooledTemporaryFile as _SpooledTemporaryFile

import dateutil.parser
from pytz import timezone

import dgi_repo.logger
from dgi_repo.configuration import configuration as _config

PID_SEPARATOR = ':'


def bootstrap():
    """
    Run code that should always be ran at the beginning of the application run.
    """
    dgi_repo.logger.configure_logging()


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
    # Because it's the first arg; if there are args the max_size is overridden.
    if args:
        spooled_file = _SpooledTemporaryFile(*args, **kwargs)
    elif 'max_size' in kwargs:
        # Favour a keyword max_size over our defaults.
        spooled_file = _SpooledTemporaryFile(**kwargs)
    else:
        spooled_file = _SpooledTemporaryFile(
            _config['spooled_temp_file_size'],
            **kwargs
        )

    return spooled_file


def iso8601_to_datetime(time):
    """
    Process an ISO 8601 string into an aware datetime.
    """
    if time is not None:
        dt = check_datetime_timezone(
            dateutil.parser.parse(time)
        )
        return dt
    return None


def check_datetime_timezone(check):
    """
    If the datetime is timezone unaware apply the configured timezone.
    """
    if check.tzinfo is None or check.tzinfo.utcoffset is None:
        our_timezone = timezone(_config['timezone'])
        check = our_timezone.localize(check)
    return check
