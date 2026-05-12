from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_usuarios, name='lista_usuarios'),
    path('crear/paso1/', views.crear_usuario_paso1, name='crear_usuario_paso1'),
    path('crear/paso2/', views.crear_usuario_paso2, name='crear_usuario_paso2'),
    path('crear/paso3/', views.crear_usuario_paso3, name='crear_usuario_paso3'),
    path('crear/paso4/', views.crear_usuario_paso4, name='crear_usuario_paso4'),
    path('crear/paso5/', views.crear_usuario_paso5, name='crear_usuario_paso5'),
    path('crear/paso6/', views.crear_usuario_paso6, name='crear_usuario_paso6'),
    path('crear/paso7/', views.crear_usuario_paso7, name='crear_usuario_paso7'),
    path('editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
]