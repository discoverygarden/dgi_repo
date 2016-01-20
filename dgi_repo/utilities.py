"""
Utility functions.
"""


def bootstrap():
    """
    Run code that should always be ran at the beginining of the application run.
    """

    import dgi_repo.logger

    dgi_repo.logger.configure_logging()
