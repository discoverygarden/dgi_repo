#!/usr/bin/env python
'''
Authorize actions.
'''

def authorize(identity, action):
    '''
    An external authorizor, as for talons.auth.external.Authorizer.

    Parameters:
        identity: A talons.auth.interfaces.Identity instance
        action: A talons.auth.interfaces.ResourceAction instance, with
            properties:
            request: The falcon.Request object representing the HTTP request and
            params: The dict of parameters.

    Returns:
        A boolean indicating if the action should be allowed by the given agent.
    '''
    return True
