from rest_framework import serializers

from exercice.models import Exercice
from users.models import User
from language.models import Language


class ExerciceDataSerializer(serializers.ModelSerializer):
    uuid_user = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )
    ex_language = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all()
    )

    class Meta:
        model = Exercice
        fields = ('uuid', 'uuid_user','name', 'describe', 'timer', 'ex_language', 'test', 'correct')
