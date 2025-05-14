import os
import uuid

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib import messages
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

from language.models import Language
from skillmatch.MasterViews.BaseView import BaseView
from exercice.models import Exercice
from exercice.serializers.ExerciceDataSerializer import ExerciceDataSerializer
from users.models import User


class ExerciceDataView(BaseView):
    serializer_class = ExerciceDataSerializer
    model_class = Exercice

    def __init__(self):
        super().__init__()

    @extend_schema(
        parameters=[
            OpenApiParameter('user_id', type=int, location=OpenApiParameter.QUERY, description="ID de l'utilisateur"),
        ]
    )
    def get(self, request):
        getuuid = request.GET.get('uuid_user')
        user_id = request.GET.get('user_id')  # Récupérer l'ID de l'utilisateur

        if getuuid is not None:
            try:
                test_exercice = Exercice.objects.get(uuid=getuuid)
                serializer = ExerciceDataSerializer(test_exercice)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exercice.DoesNotExist:
                return Response({"error": "Exercice not found"}, status=status.HTTP_404_NOT_FOUND)
        elif user_id is not None:
            try:
                # Filtrer les exercices par l'ID de l'utilisateur
                test_exercice = Exercice.objects.filter(uuid_user__id=user_id)
                serializer = ExerciceDataSerializer(test_exercice, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exercice.DoesNotExist:
                return Response({"error": "No exercices found for this user"}, status=status.HTTP_404_NOT_FOUND)
        else:
            test_exercice = Exercice.objects.all()
            serializer = ExerciceDataSerializer(test_exercice, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    @extend_schema(
        request=ExerciceDataSerializer,
        responses=ExerciceDataSerializer,
        examples=[
            OpenApiExample(
                "Exemple de requête",
                summary="Exemple de création d'exercice",
                description="Un exemple de données envoyées pour créer un nouvel exercice.",
                value={
                    "uuid_user": [],
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
        user_ids = data.get('uuid_user', [])  # Récupérer les IDs des utilisateurs

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

        # Ajouter les utilisateurs à l'exercice
        for user_id in user_ids:
            try:
                user = get_object_or_404(User, id=user_id)
                new_test.uuid_user.add(user)
            except ValueError:
                return JsonResponse({"error": f"L'ID de l'utilisateur {user_id} n'est pas valide."}, status=400)

        with open(test, "w") as file:
            file.write(data.get('Test', ''))

        serializer = ExerciceDataSerializer(new_test)
        messages.success(request, "Formulaire soumis avec succès !")
        return JsonResponse(serializer.data, safe=False)

    @extend_schema(
        parameters=[
            OpenApiParameter('uuid_user', type=str, location=OpenApiParameter.QUERY, description="UUID de l'exercice à supprimer"),
        ]
    )
    def delete(self, request):
        getuuid = request.GET.get('uuid_user')

        if getuuid is not None:
            try:
                test_exercice = Exercice.objects.get(uuid=getuuid)
                test_exercice.delete()
                return Response({"message": "Exercice deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            except Exercice.DoesNotExist:
                return Response({"error": "Exercice not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "UUID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
