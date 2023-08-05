# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: skip-file
# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class KeyMetadata(Model):
    """KeyMetadata.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id:
    :vartype id: str
    :ivar repository_id:
    :vartype repository_id: str
    :param user_role: Possible values include: 'Reader', 'Contributor',
     'Admin'
    :type user_role: str or
     ~digitaltwinrepositoryprovisioningservice.models.enum
    :ivar secret:
    :vartype secret: str
    :ivar tenant_id:
    :vartype tenant_id: str
    :ivar tenant_name:
    :vartype tenant_name: str
    :ivar created_on:
    :vartype created_on: datetime
    :ivar last_updated:
    :vartype last_updated: datetime
    :ivar connection_string:
    :vartype connection_string: str
    :ivar service_endpoint:
    :vartype service_endpoint: str
    """

    _validation = {
        'id': {'readonly': True},
        'repository_id': {'readonly': True},
        'secret': {'readonly': True},
        'tenant_id': {'readonly': True},
        'tenant_name': {'readonly': True},
        'created_on': {'readonly': True},
        'last_updated': {'readonly': True},
        'connection_string': {'readonly': True},
        'service_endpoint': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'repository_id': {'key': 'repositoryId', 'type': 'str'},
        'user_role': {'key': 'userRole', 'type': 'str'},
        'secret': {'key': 'secret', 'type': 'str'},
        'tenant_id': {'key': 'tenantId', 'type': 'str'},
        'tenant_name': {'key': 'tenantName', 'type': 'str'},
        'created_on': {'key': 'createdOn', 'type': 'iso-8601'},
        'last_updated': {'key': 'lastUpdated', 'type': 'iso-8601'},
        'connection_string': {'key': 'connectionString', 'type': 'str'},
        'service_endpoint': {'key': 'serviceEndpoint', 'type': 'str'},
    }

    def __init__(self, user_role=None):
        super(KeyMetadata, self).__init__()
        self.id = None
        self.repository_id = None
        self.user_role = user_role
        self.secret = None
        self.tenant_id = None
        self.tenant_name = None
        self.created_on = None
        self.last_updated = None
        self.connection_string = None
        self.service_endpoint = None
