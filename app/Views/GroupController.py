# from django.http import JsonResponse
# from django.contrib.auth.models import User
import pdb
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from app.serializers.Serializer import GroupSerializer
from django.contrib import messages
from drf_spectacular.openapi import AutoSchema
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from app.Models.Group import Group
from app.Models.User import User
from app.Views.Controller import Controller
from uuid import UUID
from rest_framework.response import Response
from rest_framework import status


class GroupController(Controller):
    schema = AutoSchema()
    
    def __init__(self):
        super().__init__()
    
    def get(self, request):
        # you are suppose to get groups with the ORM here
        getid = request.GET.get('id')
        # this line create a new group, its just to show you the serializer
        if getid != None :
            test_group = Group.objects.get(id=getid)
        else :
            test_group = Group.objects.all()
        # pdb.set_trace()
        return super().serialize(test_group, "user") #this route is a "user" type route, this mean only uuid will be returned, if you want to also return created_at, use "admin"
    
    @swagger_auto_schema(
        request_body=openapi.Schema(title="Création de groupe",description="Créer un groupe d'utilisateur",type=openapi.TYPE_OBJECT,required="name",
                                    properties={"name": openapi.Schema(type=openapi.TYPE_STRING, description='Nom Du Groupe'),}),
        responses={201: "Group created", 400: "Invalid input"}
    )       
    def post(self, request):
        name = request.POST.get('username') if request.POST.get('username') != None else request.data.get('name')
        new_group = Group(name=name)
        new_group.save()
        messages.success(request, "Formulaire soumis avec succès !")
        return super().serialize(new_group, "user")
    
    @swagger_auto_schema(
        request_body=GroupSerializer,  # Serializer utilisé pour documenter le corps de la requête
        responses={201: "Group modified", 400: "Invalid input"}
    )
    def put(self, request):
        uuid = request.GET.get('id') or request.data.get('uuid')
        uuid = str(UUID(uuid))
        groupname = request.POST.get('name') or request.data.get('name')
        uuidUser = request.POST.get('uuidUser') or request.data.get('uuidUser')
        group = Group.objects.get(uuid=uuid)
        group.name = groupname
        if uuidUser:
            try:
                user = User.objects.get(uuid=uuidUser)
                group.users.add(user)
            except User.DoesNotExist:
                print("")
        group.save()
        return super().serialize(group, "user")
    
    @swagger_auto_schema(
        request_body=openapi.Schema(title="Suppression de groupe",description="Supprimer un groupe d'utilisateur",type=openapi.TYPE_OBJECT,required=["uuid"],
                                    properties={"uuid": openapi.Schema(type=openapi.TYPE_STRING, description='ID Du Groupe'),}),
        responses={204: "Group Suppressed", 400: "Invalid input"}
    )   
    def delete(self, request):
        getuuid = request.GET.get('uuid') or request.data.get('uuid')
        group = Group.objects.get(uuid=getuuid)
        group.delete()
        return Response({"message": "Group Suppressed"}, status=status.HTTP_204_NO_CONTENT)
    