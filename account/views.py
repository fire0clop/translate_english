from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

def registration (request):
    if request.method == 'POST':
        username = request.POST['phone']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('main_page')
    return render(request, 'account/user_create.html')


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'account/login.html'  # Ваш шаблон для входа

    def form_valid(self, form):
        # Входим пользователя
        self.user = form.get_user()
        login(self.request, self.user)

        # Используем параметр 'next' из запроса для перенаправления пользователя
        next_url = self.request.GET.get('next', None)

        # Проверяем 'next' и перенаправляем пользователя на соответствующую страницу
        if next_url:
            return redirect(next_url)
        else:
            return reverse_lazy('main_page')
class LogoutView(LogoutView):
    next_page = reverse_lazy('main_page')