import os
from django.shortcuts import render, redirect
from app.Models.Language import Language
from django.http import HttpResponse
from app.Models.User import User

def CreateExercice(request) :
    lang = Language.objects.all()
    contexte = {
        'lang': lang
    }
    return render(request, "exercice.html",contexte)

def UploadFile(request) :
    if request.method == "POST" :
        dir = "app/exercice/python/user/"
        file = request.FILES['file']
        os.makedirs(dir, exist_ok=True)
        file_path = os.path.join(dir, file.name)
        with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        return HttpResponse("Fichier téléchargé avec succès !")
    return render(request, "upload.html")

def CreateLanguage(request) :
    return render(request, "language.html")

def Signup(request) :
    return render(request, "signup.html")

def Signin(request) :
    return render(request, "signin.html")

def SearchUser(request) :
    return render(request, "search_user.html")

def Modify(request) :
    user = request.session.get('User', '')
    contexte = {
        'User': User.objects.get(uuid=user)
    }
    return render(request, "modify.html", contexte)
