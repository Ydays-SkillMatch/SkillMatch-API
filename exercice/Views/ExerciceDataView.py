import os
import uuid

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib import messages
from drf_spectacular.utils import extend_schema, OpenApiExample

from language.models import Language
from skillmatch.MasterViews.BaseView import BaseView
from exercice.models import Exercice
from exercice.serializers import ExerciceDataSerializer


class ExerciceDataView(BaseView):
    serializer_class = ExerciceDataSerializer
    model_class = Exercice

    def __init__(self):
        super().__init__()

    def get(self, request):
        getuuid = request.GET.get('uuid')
        if getuuid is not None:
            try:
                test_exercice = Exercice.objects.get(uuid=getuuid)
            except Exercice.DoesNotExist:
                return Response({"error": "Exercice not found"}, status=404)
        else:
            test_exercice = Exercice.objects.all()
        return super().serialize(test_exercice, "user")

    @extend_schema(
        request=ExerciceDataSerializer,
        responses=ExerciceDataSerializer,
        examples=[
            OpenApiExample(
                "Exemple de requête",
                summary="Exemple de création d'exercice",
                description="Un exemple de données envoyées pour créer un nouvel exercice.",
                value={
                    "name": "Exercice Python",
                    "describe": "Résoudre un problème algorithmique",
                    "timer": 120,
                    "language": "123e4567-e89b-12d3-a456-426614174000",
                    "Test": "def test_function():\n    assert my_function(2) == 4"
                },
            )
        ]
    )
    def post(self, request):
        os.makedirs("app/exercice/python/test/", exist_ok=True)
        os.makedirs("app/exercice/python/correct/", exist_ok=True)

        data = JSONParser().parse(request)  # Parse correctement le JSON
        name = data.get('name')
        describe = data.get('describe')
        timer = data.get('timer')
        language_data = data.get('language')

        try:
            language_uuid = uuid.UUID(language_data)
        except ValueError:
            return JsonResponse({"error": "Le champ 'language' doit être un UUID valide."}, status=400)

        language = get_object_or_404(Language, uuid=language_uuid)

        uuid2 = uuid.uuid4()
        test = f"app/exercice/python/test/{uuid2}.txt"
        correct = f"app/exercice/python/correct/{uuid2}.py"

        new_test = Exercice(
            uuid=uuid2, name=name, describe=describe, timer=timer,
            ex_language=language, test=test, correct=correct
        )
        new_test.save()

        with open(test, "w") as file:
            file.write(data.get('Test', ''))

        serializer = ExerciceDataSerializer(new_test)
        messages.success(request, "Formulaire soumis avec succès !")
        return JsonResponse(serializer.data, safe=False)
