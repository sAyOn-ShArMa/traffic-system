from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('login/', views.operator_login, name='login'),
    path('register/', views.operator_register, name='register'),
    path('logout/', views.operator_logout, name='logout'),
    path('', views.command_center, name='command_center'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
