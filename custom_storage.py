from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# Locate Static Storage
class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION


# Locate Media Storage
class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION