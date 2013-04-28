"""
Serializers for data transfer of Django models into JSON/XML/YAML, etc. 
"""
from rest_framework import serializers

# Serializes a picture into its representation for transfer
class PictureSerializer(serializers.Serializer):
    id = serializers.Field(source='id')  
    dog_name = serializers.CharField(required=True, max_length=255, source='dog.name')
    url = serializers.URLField(required=True, source='image.url')
    