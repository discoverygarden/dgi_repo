"""
Utility functions.
"""


def bootstrap():
    """
    Run code that should always be ran at the beginining of the application run.
    """

    import dgi_repo.logger

    dgi_repo.logger.configure_logging()

def install():
    """
    Run code to finish installing the application.
    """

    from dgi_repo.database.utilities import install_schema

    install_schema()
