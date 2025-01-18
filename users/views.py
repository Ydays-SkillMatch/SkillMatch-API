# users/views.py
from rest_framework import generics
from .models import User
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]  # seul la personne qui a créé le compte peut le modifier
    lookup_field = 'id'  # Utiliser l'ID dans l'URL pour identifier l'utilisateur
