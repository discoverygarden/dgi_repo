#!/usr/bin/env python
'''
Authentication helpers.

Will need some means of configuring Drupal endpoints, likely as a dictionary of
dictionaries, mapping our site-identifying keys to maps of DB creds and some key
identifying the DB driver to use... And possibly the query (could we have a
default?)... Or materialization directly out of YAML (http://pyyaml.org/wiki/PyYAMLDocumentation#YAMLtagsandPythontypes)?
'''

import talons.auth.basicauth

def authenticate(identity):
    '''
    Check if the given identity is valid, and set the relevant roles.

    Likely used with talons.auth.external.Authenticator.

    Parameters:
        identity: An talons.auth.interfaces.Identity instance.

    Returns:
        A boolean indicating if the given identity authenticates.
    '''
    # TODO: Grab the config for the selected site (default if none indicated?)
    # TODO: Get a DB cursor for the selected site.
    # TODO: Check the credentials against the selected site (using provided
    # query or a default).
    return True


class SiteBasicIdentifier(talons.auth.basicauth.Identifier):
    '''
    Determine against which site to validate credentials.
    '''
    def identify(self, req):
        '''
        Look at the headers in the request for our identifying header.
        '''
        result = super().identify(req)

        if result:
            # TODO: Sniff custom header to identify the particular origin site
            # (store in "groups"?).
            pass

        return result
