from django.urls import path
from .views import UserListCreateView, UserUpdateView

urlpatterns = [
    path('me/', UserListCreateView.as_view(), name='user-list-create'),
    path('user/<int:id>/', UserUpdateView.as_view(), name='user-detail'),
]
