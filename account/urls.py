from django.urls import path,include
from .views import MyLoginView, registration, LogoutView
urlpatterns = [
    path('user-create/', registration, name = 'create-user'),
    path('login-user/', MyLoginView.as_view(), name='login-user'),
    path('logout-user/', LogoutView.as_view(), name='logout-user'),
]