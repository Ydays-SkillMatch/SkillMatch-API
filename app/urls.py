from django.urls import path, include

from app.Views.UserController import UserController
from app.Views.GroupController import GroupController
from app.Views.ExerciceController import ExerciceController
from app.Views.LanguageController import LanguageController
from app.schema import urls

urlpatterns = [
    path('users/', UserController.as_view()),
    path('groups/', GroupController.as_view()),
    path('setadmin/', UserController.put),
    path('setuser/', UserController.put),
    path('linkusertogroup/', GroupController.put),
    path('setgroup/', GroupController.put),
    path('login/', UserController.login),
    path('exercice/', ExerciceController.as_view()),
    path('language/', LanguageController.as_view()),
    path('schema/', include(urls)),
]
