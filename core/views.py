from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Usuario
from django.utils import timezone
from .forms import (
    UsuarioPaso1Form,
    UsuarioPaso2Form,
    UsuarioPaso3Form,
    UsuarioPaso4Form,
    UsuarioPaso5Form,
    UsuarioPaso6Form,
    UsuarioPaso7Form,
)


def lista_usuarios(request):
    usuarios = Usuario.objects.filter(registro_completo=True)
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})


def crear_usuario_paso1(request):
    if request.method == 'POST':
        form = UsuarioPaso1Form(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            datos['fecha_nacimiento'] = datos['fecha_nacimiento'].isoformat()
            request.session['usuario_paso1'] = datos
            return redirect('crear_usuario_paso2')
    else:
        form = UsuarioPaso1Form()
    return render(request, 'usuarios/formulario.html', {
        'form': form,
        'titulo': 'Paso 1 - Datos Personales',
    })


def crear_usuario_paso2(request):
    if not request.session.get('usuario_paso1'):
        return redirect('crear_usuario_paso1')

    if request.method == 'POST':
        form = UsuarioPaso2Form(request.POST)
        if form.is_valid():
            request.session['usuario_paso2'] = form.cleaned_data
            return redirect('crear_usuario_paso3')
    else:
        form = UsuarioPaso2Form()
    return render(request, 'usuarios/formulario.html', {
        'form': form,
        'titulo': 'Paso 2 - Datos de Contacto',
    })


def crear_usuario_paso3(request):
    if not request.session.get('usuario_paso1'):
        return redirect('crear_usuario_paso1')
    if not request.session.get('usuario_paso2'):
        return redirect('crear_usuario_paso2')

    if request.method == 'POST':
        form = UsuarioPaso3Form(request.POST)
        if form.is_valid():
            request.session['usuario_paso3'] = form.cleaned_data
            return redirect('crear_usuario_paso4')
    else:
        form = UsuarioPaso3Form()
    return render(request, 'usuarios/formulario_paso3.html', {
        'form': form,
        'titulo': 'Paso 3 - Información Médica',
    })


def crear_usuario_paso4(request):
    if not request.session.get('usuario_paso1'):
        return redirect('crear_usuario_paso1')
    if not request.session.get('usuario_paso2'):
        return redirect('crear_usuario_paso2')
    if not request.session.get('usuario_paso3'):
        return redirect('crear_usuario_paso3')

    if request.method == 'POST':
        form = UsuarioPaso4Form(request.POST)
        if form.is_valid():
            request.session['usuario_paso4'] = form.cleaned_data
            return redirect('crear_usuario_paso5')
    else:
        form = UsuarioPaso4Form()
    return render(request, 'usuarios/formulario_paso4.html', {
        'form': form,
        'titulo': 'Paso 4 - Contacto de Emergencia',
    })


def crear_usuario_paso5(request):
    pasos_previos = ['usuario_paso1', 'usuario_paso2', 'usuario_paso3', 'usuario_paso4']
    for paso in pasos_previos:
        if not request.session.get(paso):
            return redirect('crear_usuario_paso1')

    if request.method == 'POST':
        form = UsuarioPaso5Form(request.POST)
        if form.is_valid():
            request.session['usuario_paso5'] = form.cleaned_data
            return redirect('crear_usuario_paso6')
    else:
        form = UsuarioPaso5Form()
    return render(request, 'usuarios/formulario.html', {
        'form': form,
        'titulo': 'Paso 5 - Vehículo',
    })


def crear_usuario_paso6(request):
    pasos_previos = ['usuario_paso1', 'usuario_paso2', 'usuario_paso3',
                     'usuario_paso4', 'usuario_paso5']
    for paso in pasos_previos:
        if not request.session.get(paso):
            return redirect('crear_usuario_paso1')

    datos_combinados = {}
    for paso in pasos_previos:
        datos_combinados.update(request.session[paso])

    if isinstance(datos_combinados.get('fecha_nacimiento'), str):
        datos_combinados['fecha_nacimiento'] = date.fromisoformat(
            datos_combinados['fecha_nacimiento']
        )

    usuario_temp = Usuario(**datos_combinados)

    if request.method == 'POST':
        form = UsuarioPaso6Form(request.POST, request.FILES, instance=usuario_temp)
        if form.is_valid():
            usuario = form.save()
            request.session['usuario_id_creado'] = usuario.id
            return redirect('crear_usuario_paso7')  # ← antes redirigía a 'lista_usuarios'
    else:
        form = UsuarioPaso6Form(instance=usuario_temp)

    return render(request, 'usuarios/formulario_paso6.html', {
        'form': form,
        'titulo': 'Paso 6 - Documentos',
    })

def crear_usuario_paso7(request):
    usuario_id = request.session.get('usuario_id_creado')
    if not usuario_id:
        return redirect('crear_usuario_paso1')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        form = UsuarioPaso7Form(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            usuario_completo = form.save(commit=False)
            usuario_completo.fecha_aceptacion_legal = timezone.now()
            usuario_completo.registro_completo = True
            usuario_completo.save()

            # Limpiar toda la sesión del registro
            for c in ['usuario_paso1', 'usuario_paso2', 'usuario_paso3',
                      'usuario_paso4', 'usuario_paso5', 'usuario_id_creado']:
                request.session.pop(c, None)

            messages.success(request, f'Registro de {usuario_completo} completado.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioPaso7Form(instance=usuario)

    return render(request, 'usuarios/formulario_paso7.html', {
        'form': form,
        'titulo': 'Paso 7 - Aspectos Legales',
        'usuario': usuario,  # ← lo pasamos al template para interpolar nombre y cédula
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
        'titulo': 'Editar Usuario',
    })


def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')
    return render(request, 'usuarios/eliminar.html', {'usuario': usuario})