from django.urls import path

from navigator.Views import NavData

urlpatterns = [
    path('navdata/', NavData.as_view(), name='navdata-list'),
    path('navdata/<uuid:uuid>/', NavData.as_view(), name='navdata-detail'),
]