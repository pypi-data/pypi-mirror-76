"""
Wisdom is the user interaction with Whatify wisdom, it contains

"""
# Prediction is the way to productize the Ensemble created in the previous steps. Once an Ensemble is created,
# users can upload additional Datasources that may be used for predictions.
#
# ‘Prediction’ API includes querying of predictions (Get, List and Delete) and creating a Prediction to get predictions
# on existing Ensembles and uploaded Datasources.
import os
from io import StringIO
import boto3
import pandas as pd
import s3fs
import toolkit_w
from toolkit_w.internal.api_requestor import APIRequestor
from toolkit_w.internal.whatify_response import WhatifyResponse
from toolkit_w.resources.api_resource import APIResource


class Connector(APIResource):
    _CLASS_PREFIX = 'connectors'
    credentials = None
    s3_path = None
    s3_client = None

    @classmethod
    def get_credentials(cls, user_token: str = None):
        # if cls.credentials is None:
        url = '/'.join([cls._CLASS_PREFIX, 'whatify_connect_permissions'])
        requester = APIRequestor()
        if user_token is None:
            user_token = toolkit_w.token
        cls.credentials = requester.get(url, params={'jwt': user_token})
        return cls.credentials

    @classmethod
    def get_s3_path(cls, user_token: str = None):
        cls.get_credentials(user_token)
        if cls.s3_path is None:
            bucket = cls.credentials['bucket']
            PATH = cls.credentials['path']
            cls.s3_path = f's3://{bucket}/{PATH}/'
        return cls.s3_path

    @classmethod
    def get_client_path(cls, user_token: str = None):
        cls.get_credentials(user_token)
        os.environ['AWS_ACCESS_KEY_ID'] = cls.credentials['access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = cls.credentials['secret_key']
        os.environ['AWS_SESSION_TOKEN'] = cls.credentials['session_token']
        os.environ['AWS_DEFAULT_REGION'] = cls.credentials['region']
        fs = s3fs.S3FileSystem()
        return fs.ls(cls.get_s3_path(user_token=user_token))

    @classmethod
    def get_s3_boto_client(cls, user_token: str = None):
        cls.get_credentials(user_token)
        cls.s3_client = boto3.client('s3',
                                 aws_access_key_id=cls.credentials['access_key'],
                                 aws_secret_access_key=cls.credentials['secret_key'],
                                 aws_session_token=cls.credentials['session_token'])
        return cls.s3_client  # , cls.credentials['bucket'], cls.credentials['path']

    @classmethod
    def read_to_pandas_df(cls, user_token: str = None):  # s3_client, bucket, path):
        cls.get_s3_boto_client(user_token=user_token)
        obj = cls.s3_client.get_object(Bucket=cls.credentials['bucket'], Key=cls.credentials['path'])
        df = pd.read_csv(obj['Body'])
        return df

    @classmethod
    def write_pandas_df_to_s3(cls, df, user_token: str = None): # s3_client, bucket, path, df):
        s3_client = cls.get_s3_boto_client(user_token=user_token)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        s3_client.upload_fileobj(csv_buffer, Bucket=cls.credentials['bucket'], Key=cls.credentials['path'])



