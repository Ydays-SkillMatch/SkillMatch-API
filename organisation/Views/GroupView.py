from skillmatch.MasterViews.BaseView import BaseView
from organisation.models.Group import Group
from organisation.serializers.GroupSerializer import GroupSerializer
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
import json

class GroupViewList(BaseView):
    serializer_class = GroupSerializer
    model_class = Group
    
    def __init__(self):
        super().__init__()
        
    @extend_schema(
        summary="Afficher les groupes",
        description="Récupére tous les groupes",
        request=GroupSerializer,  # Utilise le serializer pour définir la structure attendue
        responses={200: GroupSerializer}
    )
    
    def get(self, request, uuid=None):
        if uuid :
            test_group = Group.objects.get(uuid=uuid)
            serializer = GroupSerializer(test_group)
        else :
            test_group = Group.objects.all()
            serializer = GroupSerializer(test_group, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @extend_schema(
        summary="Créer un groupe",
        description="Crée un nouveau groupe",
        request=GroupSerializer,  # Utilise le serializer pour définir la structure attendue
        responses={201: GroupSerializer}
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
        users = data.get('users', [])

        if not name:
            return Response({"error": "Le champ 'name' est requis."}, status=status.HTTP_400_BAD_REQUEST)

        new_group = Group.objects.create(name=name)
        if users:
            new_group.users.set(users)

        serializer = GroupSerializer(new_group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @extend_schema(exclude=True)
    def put(self, request):
        return Response({"error": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    @extend_schema(exclude=True)
    def delete(self, request):
        return Response({"error": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED) 

class GroupViewDetail(BaseView):
    serializer_class = GroupSerializer
    model_class = Group
    
    def __init__(self):
        super().__init__()
        
    @extend_schema(
        summary="Afficher un groupe",
        description="Récupére un groupe",
        request=GroupSerializer,  # Utilise le serializer pour définir la structure attendue
        responses={200: GroupSerializer}
    )
    
    def get(self, request, uuid=None):
        if uuid :
            test_group = Group.objects.get(uuid=uuid)
            serializer = GroupSerializer(test_group)
        else :
            test_group = Group.objects.all()
            serializer = GroupSerializer(test_group, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(exclude=True)
    def post(self, request):
        return Response({"error": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @extend_schema(
        summary="Modifier un groupe",
        description="Modifie un groupe",
        request=GroupSerializer,  # Utilise le serializer pour définir la structure attendue
        responses={200: GroupSerializer}
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
        users = data.get('users', [])

        if not name or not uuid:
            return Response({"error": "Le champ 'name' et 'uuid' sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        get_group = Group.objects.get(uuid=uuid)
        get_group.name = name
        if users:
            get_group.users.set(users)
        get_group.save()
        serializer = GroupSerializer(get_group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Supprimer un groupe",
        description="Supprime un groupe",
        request=GroupSerializer,  # Utilise le serializer pour définir la structure attendue
        responses={200: GroupSerializer}
    )
    
    
    def delete(self, request, uuid=None):
        if uuid :
            test_group = Group.objects.get(uuid=uuid)
            test_group.delete()
        else :
            return Response({"error": "Le Champ 'uuid' est obligatoire"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Groupe Supprimé"}, status=status.HTTP_200_OK)