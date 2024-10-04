from django.urls import path
from . import views


urlpatterns = [
    # Стартовая страница с QR-кодом
    path('qrcode/', views.qr_code_view, name='qr_code'),

    # Страница авторизации
    path('login/', views.login_view, name='login'),

    # Страница успешного входа
    path('success/', views.success_view, name='success'),
    path('logout/', views.logout_view, name='logout'),
    # Страница ошибки
    path('error/', views.error_view, name='error'),
]
