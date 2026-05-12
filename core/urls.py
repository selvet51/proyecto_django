from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.lista_usuarios,
        name='lista_usuarios'
    ),

    path(
        'crear/paso1/',
        views.crear_usuario_paso1,
        name='crear_usuario_paso1'
    ),

    path(
        'crear/paso2/',
        views.crear_usuario_paso2,
        name='crear_usuario_paso2'
    ),

    path(
        'editar/<int:id>/',
        views.editar_usuario,
        name='editar_usuario'
    ),

    path(
        'eliminar/<int:id>/',
        views.eliminar_usuario,
        name='eliminar_usuario'
    ),
]