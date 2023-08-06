from enum import Enum
from typing import NamedTuple
from datetime import datetime
from botocore.response import StreamingBody

'''
S3 Constants
=========================================================================================
Boto3 v1.9.232
Reference: 
- https://boto3.amazonaws.com/v1/documentation/api/1.9.232/reference/services/s3.html


ACL constants
===========================================================
'''


class S3Acl(Enum):
    private = 'private'
    public_read = 'public-read'
    public_read_write = 'public-read-write'
    authenticated_read = 'authenticated-read'
    aws_exec_read = 'aws-exec-read'
    bucket_owner_read = 'bucket-owner-read'
    bucket_owner_full_control = 'bucket-owner-full-control'


'''
===========================================================

Responses
===========================================================
'''


class S3GetObjectResponse(NamedTuple):
    Body: StreamingBody
    ResponseMetadata: dict
    DeleteMarker: bool = None
    AcceptRanges: str = None
    Expiration: str = None
    Restore: str = None
    LastModified: datetime = None
    ContentLength: int = None
    ETag: str = None
    MissingMeta: int = None
    VersionId: str = None
    CacheControl: str = None
    ContentDisposition: str = None
    ContentEncoding: str = None
    ContentLanguage: str = None
    ContentRange: str = None
    ContentType: str = None
    Expires: datetime = None
    WebsiteRedirectLocation: str = None
    ServerSideEncryption: str = None
    Metadata: dict = None
    SSECustomerAlgorithm: str = None
    SSECustomerKeyMD5: str = None
    SSEKMSKeyId: str = None
    StorageClass: str = None
    RequestCharged: str = None
    ReplicationStatus: str = None
    PartsCount: int = None
    TagCount: int = None
    ObjectLockMode: str = None
    ObjectLockRetainUntilDate: datetime = None
    ObjectLockLegalHoldStatus: str = None
