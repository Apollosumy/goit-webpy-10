from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # Подключаем маршруты из приложения main
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Вход
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Выход
]
