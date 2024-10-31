from django.contrib import admin
from django.urls import path, include

from app import views, urls
from app.Views.UserController import UserController
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.Signup),
    path('signin/', views.Signin),
    path('modify/', views.Modify),
    path('SearchUser/', views.SearchUser),
    path('api/', include(urls)),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    )
]