import string

from requests_aws4auth import AWS4Auth
import boto3
from elasticsearch import Elasticsearch as ES, RequestsHttpConnection

PUNC_TRANS_TABLE = str.maketrans({x: ' ' for x in string.punctuation})


def es_wrapper(endpoint: str, region: str, profile_name: str = 'default'):
    """
    Wrapper function for Elasticsearch
    """
    credentials = boto3.Session(profile_name=profile_name).get_credentials()
    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        'es',
        session_token=credentials.token
    )

    return ES(
        endpoint,
        http_auth=awsauth,
        scheme="https",
        use_ssl=False,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )


def remove_puncs_and_extra_spaces(text: str) -> str:
    return ' '.join(text.translate(PUNC_TRANS_TABLE).split()).lower()
