from django.contrib import admin
from django.urls import path
from app_sujeto import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mostrar_sujeto, name='mostrar_sujeto'),
]

