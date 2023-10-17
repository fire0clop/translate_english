from django.urls import path,include
from .views import trainer_choise, training, new_correct, new_wrong

urlpatterns = [
    path('', trainer_choise, name = 'trainer_choise'),
    path('f/', training, name = 'first_training'),
    path('new_correct/', new_correct, name = 'correct_choise'),
    path('new_wrong/', new_wrong, name = 'wrong_choise')
]