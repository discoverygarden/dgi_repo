"""
System/configured user auth functionality.
"""
import ipaddress
from ipaddress import IPv4Network, IPv4Address
from crypt import crypt

from talons.auth import interfaces

from dgi_repo.configuration import configuration as _config


def authenticate(identity):
    """
    Authenication callback.
    """
    if identity.site is not None:
        return None

    try:
        password = _config['configured_users']['users'][identity.login]
    except KeyError:
        return None
    else:
        if password == crypt(identity.key, password):
            identity.site = _config['configured_users']['source']
            return True
        return False


class Authorize(interfaces.Authorizes):
    """
    Callable authorization class.
    """
    def __init__(self):
        self._networks = IPNetworkSet(_config['configured_users']['ips'])

    def authorize(self, identity, resource):
        if identity.site == _config['configured_users']['source']:
            return resource.request.remote_addr in self._networks


class IPNetworkSet(object):
    """
    Represent a set of IP networks, both v4 and v6.
    """
    def __init__(self, ips):
        """
        Constructor.

        Params:
            ips: An iterable of network specifications in either CIDR notation
                or with the network and subnet masks separated by a slash, for
                example: 127.0.0.0/8 and 127.0.0.0/255.0.0.0 would be
                equivalent.
        """
        self._ipv4 = []
        self._ipv6 = []

        for ip in ips:
            network = ipaddress.ip_network(ip, False)
            if isinstance(network, IPv4Network):
                self._ipv4.append(network)
            else:
                self._ipv6.append(network)

        self._ipv4 = set(ipaddress.collapse_addresses(self._ipv4))
        self._ipv6 = set(ipaddress.collapse_addresses(self._ipv6))

    def __contains__(self, addr):
        """
        Test if the given IP is contained in our set of networks.
        """
        ip = ipaddress.ip_address(addr)
        networks = self._ipv4 if isinstance(ip, IPv4Address) else self._ipv6
        for net in networks:
            if ip in net:
                return True
        return False
