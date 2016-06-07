from talons.auth import interfaces


class Authenticator(interfaces.Authenticates):
    def __init__(self, *callables):
        self._callables = callables

    def authenticate(self, identity):
        result = False
        for call in self._callables:
            result = call(identity)
            if result:
                return result
        if not result:
            # If everything returned False or None, we have failed to
            # authenticate.
            return False

    def sets_group(self):
        return True
