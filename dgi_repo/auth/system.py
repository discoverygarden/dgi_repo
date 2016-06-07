from crypt import crypt

from dgi_repo.configuration import configuration as _config


def authenticate(identity):
    if identity.site is not None:
        return None

    try:
        password = _config['system_users'][identity.login]
    except KeyError:
        return None
    else:
        if password == crypt(identity.key, password):
            identity.site = _config['self']['source']
            return True
        else:
            return False
