# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import msal
from ..config import BaseConfig as CC

class AadService:
    def get_access_token():
        response = None
        try:
            authority = CC.AUTHORITY_URL.replace('organizations', CC.TENANT_ID)
            clientapp = msal.ConfidentialClientApplication(CC.CLIENT_ID, client_credential=CC.CLIENT_SECRET, authority=authority)
            response = clientapp.acquire_token_for_client(scopes=CC.SCOPE_BASE)
            try:
                return response['access_token']
            except KeyError:
                raise Exception(response['error_description'])

        except Exception as ex:
            raise Exception('Error retrieving Access token\n' + str(ex))