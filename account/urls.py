from django.urls import path,include
from .views import MyLoginView, registration, LogoutView
urlpatterns = [
    path('login-user', MyLoginView.as_view(), name = 'login-user'),
    path('user-create/', registration, name = 'create-user'),
    path('user-logout/', LogoutView.as_view(), name = 'logout-user'),
]