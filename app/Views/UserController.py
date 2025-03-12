import pdb
from drf_yasg.utils import swagger_auto_schema
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
from app.Models.User import User
from app.Views.Controller import Controller
from app.serializers.Serializer import UserSerializer, UserMSerializer
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status


class UserController(Controller):
    
    def __init__(self):
        super().__init__()
    
    def get(self, request):
        # you are suppose to get users with the ORM here
        getid = request.GET.get('id')
        # this line create a new user, its just to show you the serializer
        if getid != None :
            test_user = User.objects.get(id=getid)
        else :
            test_user = User.objects.all()
        # pdb.set_trace()
        return super().serialize(test_user, "user") #this route is a "user" type route, this mean only uuid will be returned, if you want to also return created_at, use "admin"
    
    @swagger_auto_schema(
        request_body=UserSerializer,  # Serializer utilisé pour documenter le corps de la requête
        responses={201: "New User Created", 400: "Invalid input"}
    )         
    def post(self, request):
        username = request.POST.get('username') or request.data.get('username')
        email = request.POST.get('email') or request.data.get('email')
        password = request.POST.get('password') or request.data.get('password')
        if password != None :
            hashed_password = make_password(password)
            new_user = User(username=username,email=email,password=hashed_password)
            new_user.save()
            messages.success(request, "Formulaire soumis avec succès !")
            return super().serialize(new_user, "user")
        else :
            if email == None :
                email = ""
            if username == None :
                username = ""
            test_user = User.objects.filter(username__startswith=username, email__startswith=email)
            return super().serialize(test_user, "list")
    
    @swagger_auto_schema(
        request_body=UserMSerializer,
        responses={201: "User modified", 400: "Invalid input"}
    )    
    def put(self, request):
        uuid = request.GET.get('id') or request.data.get('uuid')
        username = request.POST.get('username') or request.data.get('username')
        email = request.POST.get('email') or request.data.get('email')
        admin = request.POST.get('admin') or request.data.get('admin')
        user = User.objects.get(uuid=uuid)
        user.username = username
        user.email = email
        if admin == True:
            user.admin = True
        else:
            user.admin = False
        user.save()
        return super().serialize(user, "user")
    
    @swagger_auto_schema(
        request_body=openapi.Schema(title="Suppression d'utilisateur",description="Supprimer un utilisateur",type=openapi.TYPE_OBJECT,required=["uuid"],
                                    properties={"uuid": openapi.Schema(type=openapi.TYPE_STRING, description="ID D'un utilisateur"),}),
        responses={204: "User Suppressed", 400: "Invalid input"}
    )
    def delete(self, request):
        getid = request.GET.get('id') or request.data.get('uuid')
        test_user = User.objects.get(uuid=getid)
        test_user.delete()
        return Response({"message": "User Suppressed"}, status=status.HTTP_204_NO_CONTENT)
    
    def login(request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.get(email=email)
        if check_password(password, user.password) :
            request.session['User'] = str(user.uuid)
            return HttpResponse(f"Nom d'utilisateur : {user.username}, Email : {email}")
        else :
            return HttpResponse("None")
        