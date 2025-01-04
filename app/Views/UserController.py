import uuid
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
        get_uuid = request.GET.get('uuid')
        if get_uuid:
            group = Group.objects.get(uuid=get_uuid)
        else:
            group = Group.objects.all()
        return super().serialize(group, "user")

    def post(self, request):
        name = request.POST.get('name')
        new_group = Group(name=name)
        new_group.save()
        messages.success(request, "Formulaire soumis avec succès !")
        return super().serialize(new_group, "user")

    def set_user_to_group(self, request):
        user_uuid = request.GET.get('user_uuid')
        group_uuid = request.GET.get('group_uuid')
        try:
            user = User.objects.get(uuid=user_uuid)  # Recherche  UUID.
            group = Group.objects.get(uuid=group_uuid)  # Recherche  UUID.
            user.groups.add(group)
            group.users.add(user)
            user.save()
            group.save()
        except User.DoesNotExist:
            return HttpResponse("Utilisateur non trouvé", status=404)
        except Group.DoesNotExist:
            return HttpResponse("Groupe non trouvé", status=404)
        return HttpResponse("Utilisateur lié au groupe avec succès")

    def update_group(self, request):
        group_uuid = request.GET.get('uuid')  # Utilisation UUID
        name = request.POST.get('name')
        description = request.POST.get('description', None)
        try:
            group = Group.objects.get(uuid=group_uuid)
            group.name = name
            if description:
                group.description = description
            group.save()
        except Group.DoesNotExist:
            return HttpResponse("Groupe non trouvé", status=404)
        return HttpResponse(f"Nom du groupe mis à jour : {name}")

class UserController(Controller):
    def __init__(self):
        super().__init__()

    def get(self, request):
        get_uuid = request.GET.get('uuid')  # Utilisation UUID.
        if get_uuid:
            user = User.objects.get(uuid=get_uuid)
        else:
            user = User.objects.all()
        return super().serialize(user, "user")

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if password:
            hashed_password = make_password(password)
            new_user = User(username=username, email=email, password=hashed_password)
            new_user.save()
            messages.success(request, "Formulaire soumis avec succès !")
            return super().serialize(new_user, "user")
        else:
            return HttpResponse("Mot de passe requis", status=400)

    def update_user(self, request):
        user_uuid = request.GET.get('uuid')  #UUID
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = User.objects.get(uuid=user_uuid)
            user.username = username
            user.email = email
            user.save()
        except User.DoesNotExist:
            return HttpResponse("Utilisateur non trouvé", status=404)
        return HttpResponse(f"Utilisateur mis à jour : {username}, {email}")

    def login(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_uuid'] = str(user.uuid)  # Enregistrement de l'UUID dans la session.
                return HttpResponse(f"Connexion réussie : {user.username}, {email}")
            else:
                return HttpResponse("Mot de passe incorrect", status=401)
        except User.DoesNotExist:
            return HttpResponse("Utilisateur non trouvé", status=404)

    def toggle_admin(self, request):
        user_uuid = request.GET.get('uuid')  # Utilisation des UUID pour l'administration.
        try:
            user = User.objects.get(uuid=user_uuid)
            user.admin = not user.admin
            user.save()
        except User.DoesNotExist:
            return HttpResponse("Utilisateur non trouvé", status=404)
        return HttpResponse(f"Statut admin mis à jour : {user.admin}")

    def setAdmin(self, request):
        user_uuid = request.GET.get('uuid')  # Utilisation des UUID pour l'administration.
        try:
            user = User.objects.get(uuid=user_uuid)
            user.admin = True
            user.save()
        except User.DoesNotExist:
            return HttpResponse("Utilisateur non trouvé", status=404)
        return HttpResponse(f"Statut admin mis à jour : {user.admin}")

    def setUser(self, request):
        user_uuid = request.GET.get('uuid')  # Utilisation des UUID pour l'administration.
        try:
            user = User.objects.get(uuid=user_uuid)
            # Ajoutez ici la logique spécifique que vous souhaitez implémenter pour setUser
            user.save()
        except User.DoesNotExist:
            return HttpResponse("Utilisateur non trouvé", status=404)
        return HttpResponse(f"Utilisateur mis à jour : {user.username}")

    def delete(self, request):
        user_uuid = request.GET.get('uuid')  # Suppression par UUID.
        try:
            user = User.objects.get(uuid=user_uuid)
            user.delete()
        except User.DoesNotExist:
            return HttpResponse("Utilisateur non trouvé", status=404)
        return HttpResponse("Utilisateur supprimé")
