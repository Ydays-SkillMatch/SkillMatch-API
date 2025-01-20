from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserListCreateView, UserUpdateView, CustomTokenObtainPairView

urlpatterns = [
    path('user/', UserListCreateView.as_view(), name='user-list-create'),
    path('user/<int:id>/', UserUpdateView.as_view(), name='user-detail'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
