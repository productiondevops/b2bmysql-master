# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.



class BaseConfig(object):
    # Can be set to 'MasterUser' or 'ServicePrincipal'
    AUTHENTICATION_MODE = 'ServicePrincipal'

    # Workspace Id in which the report is present
    WORKSPACE_ID = '2009c77b-9738-4433-8b40-3b5d1d841853'
     
    # Report Id for which Embed token needs to be generated #B2C
    REPORT_ID = '21c9a08b-2d55-46af-97a7-19bd5977092b'
    #3da14145-f206-4ed0-b254-8a05bc0b6145
    # Id of the Azure tenant in which AAD app and Power BI report is hosted. Required only for ServicePrincipal authentication mode.
    TENANT_ID = '066b33d0-3b2f-4064-9390-0ea689ae0fb7'
    
    # Client Id (Application Id) of the AAD app
    CLIENT_ID = '30eec8f4-035b-46d2-9939-59d8d221d476'
    
    # Client Secret (App Secret) of the AAD app. Required only for ServicePrincipal authentication mode.
    CLIENT_SECRET = 'jai8Q~OXz8XG6yqMzBKTepfdSmDT5W9BZ3SJFcu-'
    
    # Scope Base of AAD app. Use the below configuration to use all the permissions provided in the AAD app through Azure portal.
    SCOPE_BASE = ['https://analysis.windows.net/powerbi/api/.default']
    
    # URL used for initiating authorization request
    AUTHORITY_URL = 'https://login.microsoftonline.com/organizations'
    
    # Master user email address. Required only for MasterUser authentication mode.
    POWER_BI_USER = ''
    
    # Master user email password. Required only for MasterUser authentication mode.
    POWER_BI_PASS = ''