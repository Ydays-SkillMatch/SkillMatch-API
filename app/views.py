from django.shortcuts import render, redirect
from app.Models.User import User
# from app.Forms.UserForm import CustomUserCreationForm

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