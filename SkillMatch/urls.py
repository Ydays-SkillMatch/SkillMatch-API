from django.contrib import admin
from django.urls import path, include
from app import views, urls
from app.Views.UserController import UserController


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.Signup),
    path('signin/', views.Signin),
    path('modify/', views.Modify),
    path('searchuser/', views.SearchUser),
    path('api/', include(urls)),
    path('createxercice/', views.CreateExercice),
    path('createlanguage/', views.CreateLanguage),
    path('upload/', views.UploadFile),
    path('users/', UserController.as_view())
]
