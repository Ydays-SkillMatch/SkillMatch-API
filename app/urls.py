from django.urls import path

from app.Views.UserController import UserController
from app.Views.GroupController import GroupController
from app.Views.ExerciceController import ExerciceController
from app.Views.LanguageController import LanguageController

urlpatterns = [
    path('users/', UserController.as_view()),
    path('groups/', GroupController.as_view()),
    path('setAdmin/', UserController.setAdmin),
    path('setUser/', UserController.setUser),
    path('linkUsertoGroup/', GroupController.setUserToGroup),
    path('setGroup/', GroupController.setGroup),
    path('login/', UserController.login),
    path('exercice/', ExerciceController.as_view()),
    path('language/', LanguageController.as_view()),
]
