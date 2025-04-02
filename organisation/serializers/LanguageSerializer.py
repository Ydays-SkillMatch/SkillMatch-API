from rest_framework import serializers

from organisation.models.Language import Language

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('uuid', 'name', 'extension', 'created_at')