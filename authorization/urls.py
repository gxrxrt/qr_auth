from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('auth/<int:user_id>/', views.qr_auth_view, name='qr_auth'),
    path('welcome/<int:user_id>/', views.welcome_view, name='welcome'),  # Новый маршрут для страницы приветствия
    path('logout/', views.logout_view, name='logout'),  # URL для выхода
]

