from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from app.serializers.Serializer import ExerciseSerializer
from django.contrib import messages
from app.Models.Exercice import Exercice
from app.Models.Language import Language
from app.Views.Controller import Controller
from rest_framework.decorators import action
import os
import uuid


class ExerciceController(Controller):
    
    def __init__(self):
        super().__init__()
    
    def get(self, request):
        # you are suppose to get exercices with the ORM here
        getuuid = request.GET.get('uuid')
        # this line create a new exercice, its just to show you the serializer
        if getuuid != None :
            test_exercice = Exercice.objects.get(uuid=getuuid)
            if not test_exercice:
                return Response({"error": "Exercice not found"}, status=404)
        else :
            test_exercice = Exercice.objects.all()
        return super().serialize(test_exercice, "user") #this route is a "user" type route, this mean only uuid will be returned, 
        # if you want to also return created_at, use "admin"
    
    @swagger_auto_schema(
        request_body=ExerciseSerializer,  # Serializer utilisé pour documenter le corps de la requête
        responses={201: "Exercise created", 400: "Invalid input"}
    )       
    def post(self, request):
        language_uuid = request.POST.get('language') or request.data.get('language')

        if not language_uuid:
            return Response({"error": "Language is required"}, status=400)

        try:
            if "-" in language_uuid:  # Vérifie si c'est un UUID (présence de tirets)
                language = Language.objects.get(uuid=language_uuid)
            else:  # Sinon, suppose que c'est le nom du langage
                language = Language.objects.get(name=language_uuid.upper())
        except Language.DoesNotExist:
            return Response({"error": "Language not found"}, status=400)
        
        
        os.makedirs(f"app/exercice/{language.name.lower()}/test/", exist_ok=True)
        os.makedirs(f"app/exercice/{language.name.lower()}/correct/", exist_ok=True)
        name = request.POST.get('name') if request.POST.get('name') != None else request.data.get('name')
        describe = request.POST.get('describe') if request.POST.get('describe') != None else request.data.get('describe')
        timer = request.POST.get('timer') if request.POST.get('timer') != None else request.data.get('timer')
        uuid2 = uuid.uuid4()
        test = f"app/exercice/{language.name.lower()}/test/{uuid2}.txt"
        correct = f"app/exercice/{language.name.lower()}/correct/{uuid2}.{language.extension}"
        new_test = Exercice(uuid=uuid2,name=name,describe=describe,timer=timer,ex_language=language,test=test,correct=correct)
        new_test.save()
        with open(test, "w") as file:
            file.write(request.POST.get('Test') or request.data.get('Test'))
        messages.success(request, "Formulaire soumis avec succès !")
        return super().serialize(new_test, "user")
        
    
    # def setUser(request):
    #     uuid = request.GET.get('id')
    #     username = request.POST.get('username')
    #     email = request.POST.get('email')
    #     user = User.objects.get(uuid=uuid)
    #     user.username = username
    #     user.email = email
    #     user.save()
    #     return HttpResponse(f"Nom d'utilisateur : {username}, Email : {email}")
    
    # def login(request):
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')
    #     user = User.objects.get(email=email)
    #     if check_password(password, user.password) :
    #         request.session['User'] = str(user.uuid)
    #         return HttpResponse(f"Nom d'utilisateur : {user.username}, Email : {email}")
    #     else :
    #         return HttpResponse("None")
        
    # def setAdmin(request):
    #     getid = request.GET.get('id')
    #     test_user = User.objects.get(id=getid)
    #     before = test_user.admin
    #     if test_user.admin == True :
    #         test_user.admin = False
    #     else :
    #         test_user.admin = True
    #     test_user.save()
    #     return HttpResponse(f"Avant : {before}, Maintenant : {test_user.admin}")
    
    # def delete(request):
    #     getid = request.GET.get('id')
    #     test_user = User.objects.get(id=getid)
    #     test_user.delete()
    #     return HttpResponse(f"User deleted")
    
    