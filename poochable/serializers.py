from rest_framework import serializers

class PictureSerializer(serializers.Serializer):
    id = serializers.Field(source='id')  
    dog_name = serializers.CharField(required=True, max_length=255, source='dog.name')
    url = serializers.URLField(required=True, source='image.url')
    