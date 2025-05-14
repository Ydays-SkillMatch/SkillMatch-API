from django.contrib import messages
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.parsers import JSONParser

from language.models import Language
from language.serializers.LanguageSerializer import LanguageSerializer
from skillmatch.MasterViews.BaseView import BaseView

class LanguageView(BaseView):
    serializer_class = LanguageSerializer
    model_class = Language

    def __init__(self):
        super().__init__()

    def get(self, request):
        getuuid = request.GET.get('uuid')

        if getuuid:
            # Validate UUID format before querying the database
            try:
                UUID(getuuid)  # Will raise a ValueError if not a valid UUID
                test_language = Language.objects.get(uuid=getuuid)
                serializer = LanguageSerializer(test_language)
                return JsonResponse(serializer.data, safe=False)

            except ValueError:
                return JsonResponse({"error": "Invalid UUID format."}, status=400)
            except Language.DoesNotExist:
                return JsonResponse({"error": "Language not found."}, status=404)
        else:
            # Paginate results to prevent overloading with large datasets
            page = request.GET.get('page', 1)
            per_page = 10  # You can modify this value based on your preference

            # Query the database with pagination
            test_language = Language.objects.all()[(page - 1) * per_page : page * per_page]
            serializer = LanguageSerializer(test_language, many=True)

            return JsonResponse(serializer.data, safe=False)

    @extend_schema(
        request=LanguageSerializer,
        responses=LanguageSerializer,
        examples=[
            OpenApiExample(
                "Exemple de requête",
                summary="Exemple de création d'un langage",
                description="Un exemple de données envoyées pour créer un nouveau langage.",
                value={
                    "name": "Python",
                },
            )
        ]
    )
    def post(self, request):
        # Parse le JSON de la requête
        data = JSONParser().parse(request)
        name = data.get('name')

        # Vérifie si le champ 'name' est présent
        if not name:
            return JsonResponse({"error": "'name' ne peut pas être vide."}, status=400)

        # Si tout est ok, créer un nouvel objet Language
        language = Language.objects.create(name=name)
        return JsonResponse({"message": "Langue créée avec succès", "uuid": str(language.uuid)}, status=201)
