# from django.http import JsonResponse
# from django.contrib.auth.models import User
import os
import pdb
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from app.Models.Exercice import Exercice
from app.Views.Controller import Controller


class ExerciceController(Controller):
    
    def __init__(self):
        super().__init__()
    
    def get(self, request):
        # you are suppose to get exercices with the ORM here
        getid = request.GET.get('id')
        # this line create a new exercice, its just to show you the serializer
        if getid != None :
            test_exercice = Exercice.objects.get(id=getid)
        else :
            test_exercice = Exercice.objects.all()
        return super().serialize(test_exercice, "user") #this route is a "user" type route, this mean only uuid will be returned, 
        # if you want to also return created_at, use "admin"
            
    def post(self, request):
        os.makedirs("app/exercice/python/test/", exist_ok=True)
        os.makedirs("app/exercice/python/correct/", exist_ok=True)
        name = request.POST.get('name')
        describe = request.POST.get('describe')
        timer = request.POST.get('timer')
        language = request.POST.get('language')
        test = "app/exercice/python/test/" + name + ".txt"
        correct = "app/exercice/python/correct/" + name + ".py"
        new_test = Exercice(name=name,describe=describe,timer=timer,ex_language=language,test=test,correct=correct)
        new_test.save()
        with open(test, "w") as file:
            file.write(request.POST.get('Test'))
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
    
    