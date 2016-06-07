import ipaddress
from crypt import crypt

from dgi_repo.configuration import configuration as _config

def authenticate(identity):
    if identity.site is not None:
        return None

    try:
        password = _config['self']['others']['users'][identity.login]
    except KeyError:
        return None
    else:
        if password == crypt(identity.key, password):
            identity.site = _config['self']['source']
            return True
        return False

class Authorize:
    def __init__(self):
        self._ipv4 = []
        self._ipv6 = []

        for ip in _config['self']['others']['ips']:
            try:
                self._ipv4.append(ipaddress.IPv4Network(ip, False))
            except ipaddress.AddressValueError:
                self._ipv6.append(ipaddress.IPv6Network(ip, False))

    def __call__(self, identity, resource):
        if identity.site == _config['self']['source']:
            return self._test_ip(resource.request.remote_addr)

    def _test_ip(self, remote_addr):
        try:
            ip = ipaddress.IPv4Address(remote_addr)
            for net in self._ipv4:
                if ip in net:
                    return True
        except ipaddress.AddressValueError:
            ip = ipaddress.IPv6Address(remote_addr)
            for net in self._ipv6:
                if ip in net:
                    return True
        return False
