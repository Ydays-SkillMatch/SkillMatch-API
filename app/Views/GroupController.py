from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from app.Models.Group import Group
from app.Models.User import User
from app.Views.Controller import Controller


class GroupController(Controller):

    def __init__(self):
        super().__init__()

    @swagger_auto_schema(
        operation_summary="Obtenir des groupes",
        operation_description="Récupère un ou plusieurs groupes. Vous pouvez spécifier un uuid pour récupérer un groupe spécifique.",
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_QUERY, description="ID du groupe", type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: "Liste des groupes ou détails d'un groupe",
            404: "Groupe introuvable"
        }
    )
    def get(self, request):
        getid = request.GET.get('id')
        if getid is not None:
            try:
                test_group = Group.objects.get(id=getid)
            except Group.DoesNotExist:
                return HttpResponse("Groupe introuvable", status=404)
        else:
            test_group = Group.objects.all()
        return super().serialize(test_group, "user")

    @swagger_auto_schema(
        operation_summary="Créer un nouveau groupe",
        operation_description="Créer un groupe avec un nom fourni dans le corps de la requête.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="Nom du groupe")
            },
            required=['username']
        ),
        responses={201: "Groupe créé avec succès"}
    )
    def post(self, request):
        name = request.POST.get('username')
        new_group = Group(name=name)
        new_group.save()
        messages.success(request, "Formulaire soumis avec succès !")
        return super().serialize(new_group, "user")

    @swagger_auto_schema(
        operation_summary="Associer un utilisateur à un groupe",
        manual_parameters=[
            openapi.Parameter('idUser', openapi.IN_QUERY, description="ID de l'utilisateur", type=openapi.TYPE_STRING),
            openapi.Parameter('idGroup', openapi.IN_QUERY, description="ID du groupe", type=openapi.TYPE_STRING)
        ],
        responses={200: "Utilisateur lié au groupe", 404: "Utilisateur ou groupe introuvable"}
    )
    def setUserToGroup(request):
        idUser = request.GET.get('idUser')
        idGroup = request.GET.get('idGroup')
        try:
            R_User = User.objects.get(id=idUser)
            R_Group = Group.objects.get(id=idGroup)
            R_User.groups.add(R_Group)
            R_Group.users.add(R_User)
            R_User.save()
            R_Group.save()
            return HttpResponse("Utilisateur lié")
        except (User.DoesNotExist, Group.DoesNotExist):
            return HttpResponse("Utilisateur ou groupe introuvable", status=404)

    @swagger_auto_schema(
        operation_summary="Mettre à jour un groupe",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="UUID du groupe", type=openapi.TYPE_STRING)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="Nouveau nom du groupe")
            },
            required=['name']
        ),
        responses={200: "Groupe mis à jour", 404: "Groupe introuvable"}
    )
    def setGroup(request):
        uuid = request.GET.get('id')
        username = request.POST.get('name')
        try:
            group = Group.objects.get(uuid=uuid)
            group.name = username
            group.save()
            return HttpResponse(f"Nom du groupe mis à jour : {username}")
        except Group.DoesNotExist:
            return HttpResponse("Groupe introuvable", status=404)
