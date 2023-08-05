import boto3
import base64
import math
from botocore.exceptions import ClientError
import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner
from pymongo import MongoClient
from urllib.parse import urlparse
import json



session = boto3.Session(profile_name='default') # use default aws session (session is stored in  ~/.aws/credentials)
def rsa_signer(message):
    pass

def get_cloudfront_url(url):
    pass

def get_signed_url(url):
    pass


def get_db_connection():
    pass

def get_secret(secret_name):
    pass
