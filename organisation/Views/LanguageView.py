from skillmatch.MasterViews.BaseView import BaseView
from organisation.models.Language import Language
from organisation.serializers.LanguageSerializer import LanguageSerializer
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
import json

class LanguageViewList(BaseView):
    serializer_class = LanguageSerializer
    model_class = Language
    
    def __init__(self):
        super().__init__()
        
    @extend_schema(
        summary="Afficher les langages",
        description="Récupére tous les langages",
        request=LanguageSerializer,  # Utilise le serializer pour définir la structure attendue
        responses={200: LanguageSerializer}
    )
    
    def get(self, request, uuid=None):
        if uuid :
            test_lang = Language.objects.get(uuid=uuid)
            serializer = LanguageSerializer(test_lang)
        else :
            test_lang = Language.objects.all()
            serializer = LanguageSerializer(test_lang, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @extend_schema(
        summary="Ajouter un Langage",
        description="Ajoute un nouveau langage",
        request=LanguageSerializer,  # Utilise le serializer pour définir la structure attendue
        responses={201: LanguageSerializer}
    )
        
    def post(self, request):
        print("CONTENT TYPE:", request.content_type)  # Log du type de contenu
        print("RAW BODY:", request.body)  # Log du corps brut

        if request.content_type != "application/json":
            return Response({"error": "Content-Type doit être application/json"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = request.data if isinstance(request.data, dict) else json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return Response({"error": "Format JSON invalide"}, status=status.HTTP_400_BAD_REQUEST)

        print(data)
        name = data["name"]
        extension = data["extension"]

        if not name:
            return Response({"error": "Les champs 'name' et 'extension' sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        new_Language = Language.objects.create(name=name.upper(), extension=extension.lower())

        serializer = LanguageSerializer(new_Language)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @extend_schema(exclude=True)
    def put(self, request):
        return Response({"error": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    @extend_schema(exclude=True)
    def delete(self, request):
        return Response({"error": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED) 

class LanguageViewDetail(BaseView):
    serializer_class = LanguageSerializer
    model_class = Language
    
    def __init__(self):
        super().__init__()
        
    @extend_schema(
        summary="Afficher un langage",
        description="Récupére un seul langage",
        request=LanguageSerializer,  # Utilise le serializer pour définir la structure attendue
        responses={200: LanguageSerializer}
    )
    
    def get(self, request, uuid=None):
        if uuid :
            test_lang = Language.objects.get(uuid=uuid)
            serializer = LanguageSerializer(test_lang)
        else :
            test_lang = Language.objects.all()
            serializer = LanguageSerializer(test_lang, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(exclude=True)
    def post(self, request):
        return Response({"error": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @extend_schema(
        summary="Modifier un langage",
        description="Modifie un langage ajouté",
        request=LanguageSerializer,  # Utilise le serializer pour définir la structure attendue
        responses={200: LanguageSerializer}
    )
    
    def put(self, request, uuid=None):
        if request.content_type != "application/json":
            return Response({"error": "Content-Type doit être application/json"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = request.data if isinstance(request.data, dict) else json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return Response({"error": "Format JSON invalide"}, status=status.HTTP_400_BAD_REQUEST)

        print(data)
        name = data["name"]
        extension = data["extension"]
        
        if not name or not uuid:
            return Response({"error": "Les champs 'name' et 'uuid' sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        get_language = Language.objects.get(uuid=uuid)
        get_language.name = name.upper()
        get_language.extension = extension.lower()
        get_language.save()
        serializer = LanguageSerializer(get_language)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Supprimer un langage",
        description="Supprime un langage de la liste",
        request=LanguageSerializer,  # Utilise le serializer pour définir la structure attendue
        responses={200: LanguageSerializer}
    )
    
    
    def delete(self, request, uuid=None):
        if uuid :
            test_group = Language.objects.get(uuid=uuid)
            test_group.delete()
        else :
            return Response({"error": "Le Champ 'uuid' est obligatoire"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Groupe Supprimé"}, status=status.HTTP_200_OK)