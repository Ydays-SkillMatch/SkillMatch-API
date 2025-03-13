from django.urls import path

from navigator.Views.NavDataView import NavDataView

urlpatterns = [
    path('navdata/', NavDataView.as_view(), name='navdata-list'),
    path('navdata/<uuid:uuid>/', NavDataView.as_view(), name='navdata-detail'),
]