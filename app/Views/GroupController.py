# from django.http import JsonResponse
# from django.contrib.auth.models import User
import pdb

from django.contrib import messages
from drf_spectacular.openapi import AutoSchema
from django.http import HttpResponse, JsonResponse

from app.Models.Group import Group
from app.Models.User import User
from app.Views.Controller import Controller


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
            
    def post(self, request):
        name = request.POST.get('username')
        new_group = Group(name=name)
        new_group.save()
        messages.success(request, "Formulaire soumis avec succès !")
        return super().serialize(new_group, "user")
    
    def put(self, request):
        uuid = request.GET.get('id')
        username = request.POST.get('name')
        uuidUser = request.POST.get('uuidUser')
        uuidGroup = request.POST.get('uuidGroup')
        group = Group.objects.get(uuid=uuid)
        group.name = username
        if User.objects.get(uuid=uuidUser) != None and Group.objects.get(uuid=uuidGroup) != None :
            group.users.add(User.objects.get(uuid=uuidUser))
        group.save()
        return super().serialize(group, "user")
    
    def delete(self, request):
        getuuid = request.GET.get('uuid')
        group = Group.objects.get(uuid=getuuid)
        group.delete()
        return super().serialize(group, "user")
    