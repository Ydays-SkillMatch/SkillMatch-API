# from django.http import JsonResponse
# from django.contrib.auth.models import User
import pdb
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
from app.Models.Group import Group
from app.Models.User import User
from app.Views.Controller import Controller


class GroupController(Controller):
    
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
    
    def setUserToGroup(request):
        idUser = request.GET.get('idUser')
        idGroup = request.GET.get('idGroup')
        if User.objects.get(id=idUser) != None and Group.objects.get(id=idGroup) != None :
            R_User = User.objects.get(id=idUser)
            R_Group = Group.objects.get(id=idGroup)
            R_User.groups.add(R_Group)
            R_Group.users.add(R_User)
            R_User.save()
            R_Group.save()
        else:
            return HttpResponse(f"User Non Liée")
        return HttpResponse(f"User Liée")
   
    def setGroup(request):
        uuid = request.GET.get('id')
        username = request.POST.get('name')
        group = Group.objects.get(uuid=uuid)
        group.name = username
        group.save()
        return HttpResponse(f"Nom de Groupe : {username}")
    