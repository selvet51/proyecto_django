from django.shortcuts import render, redirect, get_object_or_404

from .models import Usuario
from .forms import UsuarioPaso1Form, UsuarioPaso2Form


def lista_usuarios(request):

    usuarios = Usuario.objects.all()

    return render(request, 'usuarios/lista.html', {
        'usuarios': usuarios
    })


def crear_usuario_paso1(request):

    if request.method == 'POST':

        form = UsuarioPaso1Form(request.POST)

        if form.is_valid():

            datos = form.cleaned_data

            datos['fecha_nacimiento'] = str(
                datos['fecha_nacimiento']
            )

            request.session['usuario_paso1'] = datos

            return redirect('crear_usuario_paso2')

    else:

        form = UsuarioPaso1Form()

    return render(request, 'usuarios/formulario.html', {
        'form': form,
        'titulo': 'Paso 1 - Datos Personales'
    })


def crear_usuario_paso2(request):

    datos_paso1 = request.session.get('usuario_paso1')

    if not datos_paso1:
        return redirect('crear_usuario_paso1')

    if request.method == 'POST':

        form = UsuarioPaso2Form(request.POST)

        if form.is_valid():

            datos_completos = {
                **datos_paso1,
                **form.cleaned_data
            }

            Usuario.objects.create(**datos_completos)

            del request.session['usuario_paso1']

            return redirect('lista_usuarios')

    else:

        form = UsuarioPaso2Form()

    return render(request, 'usuarios/formulario.html', {
        'form': form,
        'titulo': 'Paso 2 - Datos de Contacto'
    })


def editar_usuario(request, id):

    usuario = get_object_or_404(Usuario, id=id)

    if request.method == 'POST':

        form = UsuarioPaso1Form(request.POST, instance=usuario)

        if form.is_valid():
            form.save()

            return redirect('lista_usuarios')

    else:

        form = UsuarioPaso1Form(instance=usuario)

    return render(request, 'usuarios/formulario.html', {
        'form': form,
        'titulo': 'Editar Usuario'
    })


def eliminar_usuario(request, id):

    usuario = get_object_or_404(Usuario, id=id)

    if request.method == 'POST':

        usuario.delete()

        return redirect('lista_usuarios')

    return render(request, 'usuarios/eliminar.html', {
        'usuario': usuario
    })