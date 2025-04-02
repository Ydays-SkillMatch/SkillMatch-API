from django.urls import path

from exercice.Views.ExerciceDataView import ExerciceDataView

urlpatterns = [
    path('exercice/', ExerciceDataView.as_view(), name='exercice-data'),
]