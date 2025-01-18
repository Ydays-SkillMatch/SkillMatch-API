from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    La permission d'accès est limitée à l'utilisateur propriétaire de l'objet.
    """

    def has_object_permission(self, request, view, obj):
        # Autoriser uniquement l'accès en lecture pour les autres utilisateurs
        if request.method in permissions.SAFE_METHODS:
            return True
        # Si la méthode n'est pas en lecture (GET, HEAD, OPTIONS), vérifier que l'utilisateur est propriétaire
        return obj == request.user
