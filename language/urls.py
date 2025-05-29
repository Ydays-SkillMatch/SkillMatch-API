from django.urls import path

from language.Views.LanguageView import LanguageView

urlpatterns = [
    path('language/', LanguageView.as_view(), name='language-data'),
]