import logging

from talons.auth import interfaces


logger = logging.getLogger(__name__)


class Authenticator(interfaces.Authenticates):
    def __init__(self, *callables):
        self._callables = callables

    def authenticate(self, identity):
        results = {call(identity) for call in self._callables}
        return True in results and False not in results

    def sets_group(self):
        return True


class Authorizor(interfaces.Authorizes):
    def __init__(self, *callables):
        self._callables = callables

    def authorize(self, identity, resource):
        results = {call(identity, resource) for call in self._callables}
        return True in results and False not in results
