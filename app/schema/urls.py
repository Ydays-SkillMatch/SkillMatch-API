from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from app.swagger import schema_view

urlpatterns = [
    path("swagger-ui/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
