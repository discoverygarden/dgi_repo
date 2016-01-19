"""
Application configuration for dgi_repo.
"""

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

with open('/etc/dgi_repo/dgi_repo.yml', 'r') as configuration_fp:
    configuration = load(configuration_fp, Loader=Loader)
