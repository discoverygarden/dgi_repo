"""
Sets up the root logger for our application.
"""

def configure_logging():
    """
    Configure logging for the application.
    """
    from logging.config import dictConfig

    from dgi_repo.configuration import configuration

    dictConfig(configuration['logging'])
