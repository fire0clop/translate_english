from django.urls import path,include
from .views import mainbase, ListBaseView, create_word, DetailBaseView, UpdateBaseView, ChangeStatusView, DeleteSelectedWordsView
urlpatterns = [
    path('', mainbase, name = 'main_base'),
    path('listbase/', ListBaseView.as_view(), name = 'list_base'),
    path('createword/', create_word, name = 'create_base'),
    path('detail/<int:pk>/', DetailBaseView.as_view(), name = 'detail_word'),
    path('detail/<int:pk>/update', UpdateBaseView.as_view(), name = 'update_word'),
    path('change_status/', ChangeStatusView.as_view(), name='change_status'),
    path ('delete_word/', DeleteSelectedWordsView.as_view(), name = 'delete_selected_word')
]