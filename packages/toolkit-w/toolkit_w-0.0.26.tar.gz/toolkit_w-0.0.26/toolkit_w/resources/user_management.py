"""
Wisdom is the user interaction with Whatify wisdom, it contains

"""
# Prediction is the way to productize the Ensemble created in the previous steps. Once an Ensemble is created,
# users can upload additional Datasources that may be used for predictions.
#
# ‘Prediction’ API includes querying of predictions (Get, List and Delete) and creating a Prediction to get predictions
# on existing Ensembles and uploaded Datasources.
import os

import s3fs

import toolkit_w
from toolkit_w.internal.api_requestor import APIRequestor
from toolkit_w.internal.whatify_response import WhatifyResponse
from toolkit_w.resources.api_resource import APIResource


class UserManagement(APIResource):
    _CLASS_PREFIX = ''

    @classmethod
    def login(cls, email: str, password: str) -> WhatifyResponse:
        """
        Authenticates user and stores temporary token in `toolkit_w.token`.

        Other modules automatically detect if a token exists and use it, unless a user specifically provides a token
        for a specific request.
        The token is valid for a 24-hour period, after which this method needs to be called again in order to generate
        a new token.

        Args:
            email (str): email.
            password (str): Password.

        Returns:
            WhatifyResponse: Empty WhatifyResponse if successful, raises FireflyError otherwise.
        """
        url = 'login'

        requestor = APIRequestor()
        response = requestor.post(url, body={'username': email, 'password': password, 'tnc': None}, api_key="")
        toolkit_w.token = response['token']
        print(' '.join(['user mail:', str(email), '- Login successful']))

        return WhatifyResponse(status_code=response.status_code, headers=response.headers)

    @classmethod
    def impersonate(cls, user_id: str = None, email: str = None, admin_token: str = None) -> WhatifyResponse:
        """
       impersonate user and stores temporary token in `toolkit_w.token`

       Args:
           user_id (str): user ID.
           email (str): User email.
           admin_token (str): Admin user token.

       Returns:
           WhatifyResponse: Empty WhatifyResponse if successful, raises WhatifyError otherwise.
       """
        if email:
            user_id = None
            raise Exception('TODO: need tom implement get user ID from mail')

        url = ''.join(['users/login_as/', str(user_id)])
        requester = APIRequestor()
        response = requester.post(url, api_key=admin_token)
        toolkit_w.token = response['result']
        print(' '.join(['user ID:', str(user_id), '- Login successful']))
        return WhatifyResponse(status_code=response.status_code, headers=response.headers)

