from rest_framework import serializers

from exercice.models import Exercice

class ExerciceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercice
        fields = 'uuid, name, describe, timer, ex_language, test, correct'
