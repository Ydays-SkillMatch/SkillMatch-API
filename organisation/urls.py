from django.urls import path

from organisation.Views.GroupView import GroupViewList
from organisation.Views.GroupView import GroupViewDetail
from organisation.Views.LanguageView import LanguageViewList
from organisation.Views.LanguageView import LanguageViewDetail

urlpatterns = [
    path('group/', GroupViewList.as_view(), name='group-list'),
    path('group/<uuid:uuid>/', GroupViewDetail.as_view(), name='group-detail'),
    path('language/', LanguageViewList.as_view(), name='language-list'),
    path('language/<uuid:uuid>/', LanguageViewDetail.as_view(), name='language-detail'),
]