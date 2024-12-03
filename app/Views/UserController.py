import pdb
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
from app.Models.User import User
from app.Views.Controller import Controller


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
            
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
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
        
    
    def setUser(request):
        uuid = request.GET.get('id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        user = User.objects.get(uuid=uuid)
        user.username = username
        user.email = email
        user.save()
        return HttpResponse(f"Nom d'utilisateur : {username}, Email : {email}")
    
    def login(request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.get(email=email)
        if check_password(password, user.password) :
            request.session['User'] = str(user.uuid)
            return HttpResponse(f"Nom d'utilisateur : {user.username}, Email : {email}")
        else :
            return HttpResponse("None")
        
    def setAdmin(request):
        getid = request.GET.get('id')
        test_user = User.objects.get(id=getid)
        before = test_user.admin
        if test_user.admin == True :
            test_user.admin = False
        else :
            test_user.admin = True
        test_user.save()
        return HttpResponse(f"Avant : {before}, Maintenant : {test_user.admin}")
    
    def delete(request):
        getid = request.GET.get('id')
        test_user = User.objects.get(id=getid)
        test_user.delete()
        return HttpResponse(f"User deleted")
    
    
