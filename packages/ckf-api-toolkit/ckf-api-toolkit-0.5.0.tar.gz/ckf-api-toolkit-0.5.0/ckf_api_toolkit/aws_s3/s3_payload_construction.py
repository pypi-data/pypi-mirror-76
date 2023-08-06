from ckf_api_toolkit.aws_s3.s3_constants import S3Acl

'''
S3 Actor Payloads
===========================================================
General
============================
'''


class S3Payload:
    pass


class S3BucketPayload(S3Payload):
    Bucket: str

    def add_bucket_name(self, bucket_name: str):
        self.Bucket = bucket_name


class S3KeyPayload(S3BucketPayload):
    Key: str

    def add_key(self, key: str):
        self.Key = key


class S3AclPayload(S3Payload):
    ACL: str

    def add_acl(self, acl: S3Acl):
        self.ACL = acl.value


class S3BodyPayload(S3Payload):
    Body: bytes

    def add_body(self, body: bytes):
        self.Body = body


class S3CacheControlPayload(S3Payload):
    CacheControl: str

    def add_cache_control(self, cache_control: str):
        self.CacheControl = cache_control


class S3ContentTypePayload(S3Payload):
    ContentType: str

    def add_content_type(self, content_type_str: str):
        self.ContentType = content_type_str


'''
============================

Get Object
============================
'''


class S3GetObjectPayload(S3KeyPayload):
    pass


'''
============================

Put Object
============================
'''


class S3PutObjectPayload(S3BodyPayload, S3AclPayload, S3KeyPayload, S3CacheControlPayload, S3ContentTypePayload):
    pass


'''
============================

Delete  Object
============================
'''


class S3DeleteObjectPayload(S3KeyPayload):
    pass
