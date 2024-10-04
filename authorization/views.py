from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from urllib3 import request
from django.contrib.auth import login


from .models import CustomUser
from io import BytesIO
import qrcode
from base64 import b64encode
from .forms import LoginForm
from django.contrib.auth import logout, authenticate


# Генерация страницы с QR-кодом
def qr_code_view(request):
    # Генерируем QR-код, который ведет на страницу авторизации
    qr_url = request.build_absolute_uri('/login/')
    qr_img = qrcode.make(qr_url)

    # Преобразуем изображение QR-кода в base64
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    img_data = b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'templates/qrcode.html', {'qr_code': img_data})

# Страница авторизации
def login_view(request):
    # Если пользователь уже авторизован, делаем редирект на главную страницу
    if request.user.is_authenticated:
        return redirect('success')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_staff:
                    login(request, user)  # Обязательно авторизуем пользователя
                    return redirect('success')  # Замените 'success' на нужный URL после успешного логина
                else:
                    return render(request, 'error.html', {'message': 'Authorization failed. Status is False.'})
            else:
                return render(request, 'error.html', {'message': 'Invalid login or password.'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

# class MyLoginView(LoginView):
#     redirect_authenticated_user = True
#     template_name = 'templates/login.html'
#     form_class = LoginForm
#
#     def form_valid(self, form):
#         # Получаем пользователя после успешной проверки формы
#         user = form.get_user()
#
#         # Авторизуем пользователя
#         login(self.request, user)
#
#         # Проверяем статус пользователя is_staff
#         if user.is_staff:  # Если пользователь - сотрудник
#             return redirect('success')  # Перенаправление на страницу успеха
#         else:
#             return redirect('error')  # Перенаправление на страницу ошибки
#

# Страница успешного входа
@login_required
def success_view(request):
    return render(request, 'templates/success.html')

# Страница ошибки
@login_required
def error_view(request):
    return render(request, 'templates/error.html', {'message': 'Your account does not have access.'})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout
