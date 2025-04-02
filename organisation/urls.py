from django.urls import path

from organisation.Views.GroupView import GroupViewList
from organisation.Views.GroupView import GroupViewDetail

urlpatterns = [
    path('group/', GroupViewList.as_view(), name='group-list'),
    path('group/<uuid:uuid>/', GroupViewDetail.as_view(), name='group-detail'),
]