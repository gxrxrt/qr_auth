from django.http import HttpResponse
from .forms import LoginForm
import qrcode
from io import BytesIO
import base64
from django.shortcuts import render, get_object_or_404
from .models import CustomUser
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            try:
                user = CustomUser.objects.get(login=login, password=password)
                if user.status:
                    # Генерация уникальной ссылки с ID пользователя
                    user_id = user.id
                    url = f"http://127.0.0.1/welcome/{user_id}/"  # Изменяем URL

                    # Генерация QR-кода
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data(url)
                    qr.make(fit=True)

                    # Создание изображения QR-кода
                    img = qr.make_image(fill='black', back_color='white')
                    buffer = BytesIO()
                    img.save(buffer, format="PNG")
                    buffer.seek(0)

                    # Преобразование изображения в base64
                    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

                    return render(request, 'success.html', {'img_data': img_base64})
                else:
                    return render(request, 'error.html', {'message': 'Authorization failed. Status is False.'})
            except CustomUser.DoesNotExist:
                return render(request, 'error.html', {'message': 'Invalid login or password.'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def qr_auth_view(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        if user.status:
            return HttpResponse('Successful authentication via QR code.')
        else:
            return HttpResponse('Error: Unauthorized user.')
    except CustomUser.DoesNotExist:
        return HttpResponse('Error: User does not exist.')


def welcome_view(request, user_id):
    # Получаем пользователя по ID
    user = get_object_or_404(CustomUser, id=user_id)

    # Отображаем страницу с приветствием
    return render(request, 'templates/authorizxation.html', {'userName': user.login})


def logout_view(request):
    # Очистка сессии
    request.session.flush()
    return redirect('login')

