"""
utils.py
Utility functions for S3 interaction and file management for Lambda.
"""
import boto3
import os
import tempfile
from urllib.parse import urlparse

s3_client = boto3.client("s3")

def download_from_s3(s3_uri, local_path=None):
    """Download a file from S3 URI to a local path. Returns the local path."""
    parsed = urlparse(s3_uri)
    bucket = parsed.netloc
    key = parsed.path.lstrip("/")
    if not local_path:
        local_path = os.path.join(tempfile.gettempdir(), os.path.basename(key))
    s3_client.download_file(bucket, key, local_path)
    return local_path

def upload_to_s3(local_path, s3_uri):
    """Upload a local file to S3 URI."""
    parsed = urlparse(s3_uri)
    bucket = parsed.netloc
    key = parsed.path.lstrip("/")
    s3_client.upload_file(local_path, bucket, key)
    return s3_uri

def is_s3_uri(uri):
    return uri.startswith("s3://")
