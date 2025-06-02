from skillmatch.MasterViews.BaseView import BaseView
from organisation.models.Group import Group
from organisation.serializers.GroupSerializer import GroupSerializer
from organisation.serializers.GroupSerializer import GroupsSerializer
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from users.models import User
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
        users_data = data.get('users', [])
        owner_data = data.get('owner')  # Récupérer le propriétaire s'il est fourni

        if not name:
            return Response({"error": "Le champ 'name' est requis."}, status=status.HTTP_400_BAD_REQUEST)

        new_group = Group.objects.create(name=name)
        
        # Gérer le propriétaire du groupe
        owner = None
        if owner_data:
            if isinstance(owner_data, dict):
                # Si c'est un dictionnaire, essayez de trouver l'utilisateur par email
                email = owner_data.get('email')
                if email:
                    try:
                        owner = User.objects.get(email=email)
                        new_group.owner = owner
                    except User.DoesNotExist:
                        pass  # Ignorer si le propriétaire n'existe pas
            elif isinstance(owner_data, int):
                # Si c'est un ID (entier), utilisez-le directement
                try:
                    owner = User.objects.get(id=owner_data)
                    new_group.owner = owner
                except User.DoesNotExist:
                    pass  # Ignorer si le propriétaire n'existe pas
        
        # Traitez les données utilisateur
        if users_data:
            user_instances = []
            for user_data in users_data:
                if isinstance(user_data, dict):
                    # Si c'est un dictionnaire, essayez de trouver l'utilisateur par email
                    email = user_data.get('email')
                    if email:
                        try:
                            user = User.objects.get(email=email)
                            user_instances.append(user)
                        except User.DoesNotExist:
                            pass  # Ignorer les utilisateurs qui n'existent pas
                elif isinstance(user_data, int):
                    # Si c'est un ID (entier), utilisez-le directement
                    try:
                        user = User.objects.get(id=user_data)
                        user_instances.append(user)
                    except User.DoesNotExist:
                        pass  # Ignorer les ID qui n'existent pas
            
            # Définir les utilisateurs du groupe
            if user_instances:
                new_group.users.set(user_instances)
                
                # Si aucun propriétaire n'a été spécifié et que la liste d'utilisateurs n'est pas vide,
                # considérer le premier utilisateur comme propriétaire
                if not owner and user_instances:
                    new_group.owner = user_instances[0]
        
        new_group.save()
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
        users_data = data.get('users', [])
        owner_data = data.get('owner')  # Récupérer le propriétaire s'il est fourni

        if not name or not uuid:
            return Response({"error": "Le champ 'name' et 'uuid' sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            get_group = Group.objects.get(uuid=uuid)
            get_group.name = name
            
            # Gérer le propriétaire du groupe
            if owner_data:
                owner = None
                if isinstance(owner_data, dict):
                    # Si c'est un dictionnaire, essayez de trouver l'utilisateur par email
                    email = owner_data.get('email')
                    if email:
                        try:
                            owner = User.objects.get(email=email)
                            get_group.owner = owner
                        except User.DoesNotExist:
                            pass  # Ignorer si le propriétaire n'existe pas
                elif isinstance(owner_data, int):
                    # Si c'est un ID (entier), utilisez-le directement
                    try:
                        owner = User.objects.get(id=owner_data)
                        get_group.owner = owner
                    except User.DoesNotExist:
                        pass  # Ignorer si le propriétaire n'existe pas
            
            # Traitez les données utilisateur
            if users_data:
                user_instances = []
                for user_data in users_data:
                    if isinstance(user_data, dict):
                        # Si c'est un dictionnaire, essayez de trouver l'utilisateur par email
                        email = user_data.get('email')
                        if email:
                            try:
                                user = User.objects.get(email=email)
                                user_instances.append(user)
                            except User.DoesNotExist:
                                pass  # Ignorer les utilisateurs qui n'existent pas
                    elif isinstance(user_data, int):
                        # Si c'est un ID (entier), utilisez-le directement
                        try:
                            user = User.objects.get(id=user_data)
                            user_instances.append(user)
                        except User.DoesNotExist:
                            pass  # Ignorer les ID qui n'existent pas
                
                # Définir les utilisateurs du groupe
                if user_instances:
                    get_group.users.set(user_instances)
                    
                    # Si aucun propriétaire n'a été spécifié jusqu'à présent et que le groupe n'a pas de propriétaire
                    if not owner_data and get_group.owner is None and user_instances:
                        get_group.owner = user_instances[0]
                    
            get_group.save()
            serializer = GroupSerializer(get_group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Groupe non trouvé"}, status=status.HTTP_404_NOT_FOUND)
    
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
    

class GroupViewUser(BaseView):
    serializer_class = GroupsSerializer
    model_class = Group
    
    def __init__(self):
        super().__init__()
        
    @extend_schema(
        summary="Afficher un ou plusieurs groupes en fonction de L'user",
        description="Récupére un ou plusieurs groupes selon l'utilisateur",
        request=GroupsSerializer,  # Utilise le serializer pour définir la structure attendue
        responses={200: GroupsSerializer}
    )
    
    def get(self, request, id=None):
        if id :
            user = get_object_or_404(User, id=id)
            test_group = Group.objects.filter(users=user)
            serializer = GroupsSerializer(test_group, many=True)
        else :
            test_group = None
            serializer = GroupsSerializer(test_group, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(exclude=True)
    def post(self, request):
        return Response({"error": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @extend_schema(exclude=True)
    def put(self, request):
        return Response({"error": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @extend_schema(exclude=True)
    def delete(self, request):
        return Response({"error": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)