"""
Serializers for data transfer of Django models into JSON/XML/YAML, etc. 
"""
from rest_framework import serializers

# Serializes a picture into its representation for transfer
class PictureSerializer(serializers.Serializer):
    id = serializers.Field(source='id')  
    share_title = serializers.CharField(required=True, max_length=255, source='share.title')
    share_content = serializers.CharField(required=False, max_length=2000, source='share.content')
    url = serializers.CharField(required=False, max_length=255, source='image.url')
    thumbnail_url = serializers.CharField(required=False, max_length=255, source='thumbnail.url')
    