from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
	location = settings.AWS_STATIC_LOCATION

class MediaStorage(S3Boto3Storage):
    location = settings.AWS_MEDIA_LOCATION
    file_overwrite = False #not to override files with same name
    default_acl = 'private' #access control list permission is set to be private
    custom_domain = False

class PublicStorage(S3Boto3Storage):
	location = settings.AWS_PUBLIC_LOCATION
	file_overwrite = False