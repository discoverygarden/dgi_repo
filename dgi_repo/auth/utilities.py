"""
Auth utility classes and functions.

We need our own Authenticator and Authorizer implementations to facilite the
the combination of results from multiple sources.
"""
from talons.auth import interfaces


def _call_until_false(callables, *args, **kwargs):
    """
    Helper; call callables until one returns False.

    Params:
        callables: An iterable of callables.
        args: Positional args to pass to each callable.
        kwargs: Keyword args to pass to each callable.

    Yields:
        The results of callables passed args and kwargs, until one is False.
        After yielding the False, we will exit.
    """
    for call in callables:
        result = call(*args, **kwargs)
        yield result
        if result is False:
            return


class Authenticator(interfaces.Authenticates):
    """
    Talons authentication wrappers.
    """
    def __init__(self, *callables):
        """
        Constructor.

        Params:
            callables: Talons authentication callbacks, accepting the identity
                object and returning True to permit, False to deny, or None to
                make no assertion.
        """
        self._callables = callables

    def authenticate(self, identity):
        """
        Top-level authentication callback.

        Defers calls to those taken in in the constructor.

        Returns:
            True if one of the callables returned True, and none returned
            False; otherwise, False.
        """
        results = set(_call_until_false(self._callables, identity))
        return True in results and False not in results

    def sets_group(self):
        """
        Indicate that callables passed may adjust groups set on the identity.
        """
        return True


class Authorizer(interfaces.Authorizes):
    def __init__(self, *callables):
        """
        Constructor.

        Params:
            callables: Talons authorization callbacks, accepting the identity
                object and returning True to permit, False to deny, or None to
                make no assertion.
        """
        self._callables = callables

    def authorize(self, identity, resource):
        """
        Top-level authorization callback.

        Defers calls to those taken in in the constructor.

        Returns:
            True if one of the callables returned True, and none returned
            False; otherwise, False.
        """
        results = set(_call_until_false(self._callables, identity, resource))
        return True in results and False not in results
