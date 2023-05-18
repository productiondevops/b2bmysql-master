# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from .aadservice import AadService
from core.modelintegrate.embedconfig import  EmbedConfig
from core.modelintegrate.embedtoken import  EmbedToken
from core.modelintegrate.reportconfig import  ReportConfig
from core.modelintegrate.embedtokenrequestbody import EmbedTokenRequestBody
# from models.reportconfig import  ReportConfig
# from models.embedtoken import EmbedToken
# from models.embedconfig import EmbedConfig
# from models.embedtokenrequestbody import EmbedTokenRequestBody
#from flask import current_app as app, abort
import requests
import json
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator

class ReportConfig:

    # Camel casing is used for the member variables as they are going to be serialized and camel case is standard for JSON keys

    reportId = None
    reportName = None
    embedUrl = None
    datasetId = None

    def __init__(self, report_id, report_name, embed_url, dataset_id = None):
        self.reportId = report_id
        self.reportName = report_name
        self.embedUrl = embed_url
        self.datasetId = dataset_id

# class SathishClass:
#     print('hiclass')
#     def hiclass():
#         print('method sathish')
        

class PbiEmbedService:
    print('Inside n')
    def Test():
        print('Test')
    
    def get_embed_params_for_single_report(self, workspace_id, report_id, additional_dataset_id=None):
        print('Inside method')
        '''Get embed params for a report and a workspace

        Args:
            workspace_id (str): Workspace Id
            report_id (str): Report Id
            additional_dataset_id (str, optional): Dataset Id different than the one bound to the report. Defaults to None.

        Returns:
            EmbedConfig: Embed token and Embed URL
        '''

        report_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}' 
              
        api_response = requests.get(report_url, headers=self.get_request_header())

        # if api_response.status_code != 200:
        #     abort(api_response.status_code, description=f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')

        api_response = json.loads(api_response.text)
        report = ReportConfig(api_response['id'], api_response['name'], api_response['embedUrl'])
        dataset_ids = [api_response['datasetId']]

        # Append additional dataset to the list to achieve dynamic binding later
        if additional_dataset_id is not None:
            dataset_ids.append(additional_dataset_id)

        embed_token = self.get_embed_token_for_single_report_single_workspace(report_id, dataset_ids, workspace_id)
        embed_config = EmbedConfig(embed_token.tokenId, embed_token.token, embed_token.tokenExpiry, [report.__dict__])
        return json.dumps(embed_config.__dict__)
    
    def get_embed_token_for_single_report_single_workspace(self, report_id, dataset_ids, target_workspace_id=None):
        '''Get Embed token for single report, multiple datasets, and an optional target workspace

        Args:
            report_id (str): Report Id
            dataset_ids (list): Dataset Ids
            target_workspace_id (str, optional): Workspace Id. Defaults to None.

        Returns:
            EmbedToken: Embed token
        '''

        request_body = EmbedTokenRequestBody()

        for dataset_id in dataset_ids:
            request_body.datasets.append({'id': dataset_id})

        request_body.reports.append({'id': report_id})

        if target_workspace_id is not None:
            request_body.targetWorkspaces.append({'id': target_workspace_id})

        # Generate Embed token for multiple workspaces, datasets, and reports. Refer https://aka.ms/MultiResourceEmbedToken
        embed_token_api = 'https://api.powerbi.com/v1.0/myorg/GenerateToken'
        api_response = requests.post(embed_token_api, data=json.dumps(request_body.__dict__), headers=self.get_request_header())

        api_response = json.loads(api_response.text)
        embed_token = EmbedToken(api_response['tokenId'], api_response['token'], api_response['expiration'])
        return embed_token
    
    def get_request_header(self):
        '''Get Power BI API request header

        Returns:
            Dict: Request header
        '''
        print('PowerBi')
        return {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + AadService.get_access_token()}