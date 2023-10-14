from .views import trainer_choise
from django.urls import path,include
urlpatterns = [
    path('', trainer_choise, name = 'trainer_choise')
]