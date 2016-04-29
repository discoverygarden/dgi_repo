"""
Installation functions.
"""
import dgi_repo.database.install as db_install


def install():
    """
    Run code to finish installing the application.
    """
    db_install.install_schema()
    db_install.install_base_data()
