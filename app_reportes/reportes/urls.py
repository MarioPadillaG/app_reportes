from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='reportes/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('', views.lista_reportes, name='lista_reportes'),
    path('nuevo/', views.crear_reporte, name='crear_reporte'),
    path('editar/<int:pk>/', views.editar_reporte, name='editar_reporte'),
    path('eliminar/<int:pk>/', views.eliminar_reporte, name='eliminar_reporte'),
    path('estado/<int:pk>/', views.cambiar_estado, name='cambiar_estado')
]