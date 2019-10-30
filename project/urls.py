from django.contrib import admin
from django.urls import path, include
from apps.cliente import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('register.urls')),
    path(r'^cliente/', include('apps.cliente.urls')),
]