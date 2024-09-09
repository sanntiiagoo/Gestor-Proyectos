
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import User
from django.contrib import messages
import re
from django.contrib.auth import authenticate, login as auth_login, logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

#----------------Inicio----------------
def home(request):
    return render(request, 'index.html')

#----------------Login----------------
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Inicio sesion correctamente.')
            return redirect('proyectos')  # Redirige a la vista de proyectos si el login es exitoso
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')
    return render(request, 'login.html')

#----------------Registro----------------

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        location = request.POST['location']
        number_phone = request.POST['number_phone']

        # Validar que el nombre de usuario no contenga números
        if any(char.isdigit() for char in username):
            messages.error(request, 'El nombre de usuario no puede contener números.')
            return render(request, 'registro.html')

        # Validar que la contraseña tenga entre 7 y 20 caracteres
        if len(password) < 7 or len(password) > 20:
            messages.error(request, 'La contraseña debe tener entre 7 y 20 caracteres.')
            return render(request, 'registro.html')
        
        # Validar que la contraseña coincida con la confirmación
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html')

        # Validar que el email sea un correo
        try:
            validate_email(email)  # Verifica el email
        except ValidationError:
            messages.error(request, 'El email no cumple con los parámetros @.')
            return render(request, 'registro.html')

        # Verifica usuario y email
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso. Por favor, elige otro.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado. Por favor, usa otro.')
        else:
            # Crea el usuario si no están en uso
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            auth_login(request, user)
            messages.success(request, 'Registrado correctamente.')
            return redirect('proyectos')  # Redirige a la vista 'home' después del registro exitoso

    return render(request, 'registro.html')

#-----------ver los proyectos------------
@login_required(login_url="login")
def verproyectos(request):
    return render(request, 'verproyectos.html')

#----------------LOGOUT----------------
def exit(request):
        logout(request)
        return redirect('home')
#----------------Vista de proyectos----------------
@login_required(login_url="login")
def proyectos(request):
    return render(request,'vistaprojectos.html')
#----------------Actualizar perfil----------------

@login_required(login_url="login")
def actualizarperfil(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        number_phone = request.POST.get('number_phone')
        location = request.POST.get('location')
        password = request.POST.get('password')
        current_password = request.POST.get('current_password')  # Campo para la contraseña actual

        user = request.user
        if username != user.username or email != user.email or number_phone != user.number_phone or location != user.location or password:
            # Validaciones
            if username != user.username:
                if not re.match(r'^[a-zA-Z]{8,50}$', username):
                    messages.error(request, 'El nombre de usuario debe tener entre 8 y 50 caracteres y no puede contener espacios ni números.')
                    return redirect('actualizar_perfil')

            if email != user.email:
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                    messages.error(request, 'Por favor, ingresa un correo electrónico válido.')
                    return redirect('actualizar_perfil')

            if password and (len(password) < 7 or len(password) > 20):
                messages.error(request, 'La contraseña debe tener entre 7 y 20 caracteres.')
                return redirect('actualizar_perfil')

            if number_phone != user.number_phone:
                if not re.match(r'^\d{2}\d{10}$', number_phone):
                    messages.error(request, 'El número de teléfono debe tener 12 dígitos, incluyendo el código de país.')
                    return redirect('actualizar_perfil')

            if location != user.location:
                if not re.match(r'^[a-zA-Z\s]{4,20}$', location):
                    messages.error(request, 'El lugar de residencia debe tener entre 4 y 20 caracteres y no incluir caracteres especiales.')
                    return redirect('actualizar_perfil')

            # Verificación de contraseña actual antes de cambiarla
            if password:
                if current_password:
                    if not user.check_password(current_password):
                        messages.error(request, 'La contraseña actual no es correcta.')
                        return redirect('actualizar_perfil')
                    user.set_password(password)
                    
                else:
                    messages.error(request, 'Ingrese la contraseña actual para cambiar la contraseña')
                    return redirect('actualizar_perfil')

            # Actualizar los campos del usuario
            user.username = username
            user.email = email
            user.number_phone = number_phone
            user.location = location
            user.save()
            auth_login(request, user)

            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('proyectos')  # Redirige de vuelta a la página de perfil
        else:
            messages.info(request, 'No hubo ningun cambio en tu perfil.')
            return redirect('proyectos')  # Redirige de vuelta a la página de perfil

    return render(request, 'perfilconfig.html')  # Asegúrate de que este nombre coincida con tu archivo de plantilla

@login_required
def crearprojectos(request):
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            #fecha_inicio = request.POST.get('fecha_inicio')
            #fecha_fin = request.POST.get('fecha_fin')

            #Validar nombre y descripcion no esten vacios
            if not nombre or not descripcion:
                messages.error(request, 'Por favor, ingresa un nombre y una descripción.')
                return redirect('crearprojectos')
            
            #Crear y guardar proyecto
            Proyecto.objects.create(nombre=nombre, descripcion=descripcion, creador=request.user)
            messages.success(request, 'Proyecto creado exitosamente.')

            return redirect('proyectos')  # Redirige a la lista de proyectos
        
        
        return render(request, 'crearprojectos.html')

@login_required
def actualizar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    # Verificar si el usuario tiene permiso para actualizar el proyecto
    if request.user != proyecto.administrador:
        return HttpResponseForbidden("No tienes permiso para actualizar este proyecto.")

    if request.method == "POST":
        form = ProyectoForm(request.POST, instance=proyecto)
        
        if form.is_valid():
            # Verificar cambios
            cambios = {}
            proyecto_actualizado = form.save(commit=False)
            
            if proyecto.nombre != proyecto_actualizado.nombre:
                cambios['nombre'] = (proyecto.nombre, proyecto_actualizado.nombre)
            if proyecto.descripcion != proyecto_actualizado.descripcion:
                cambios['descripcion'] = (proyecto.descripcion, proyecto_actualizado.descripcion)

            
            # Guardar el proyecto si todo está validado correctamente
            proyecto_actualizado.save()

            # Registrar cambios si hubo alguno
            if cambios:
                ProyectoUpdateLog.objects.create(
                    proyecto=proyecto_actualizado,
                    usuario=request.user,
                    cambios=cambios
                )
                messages.success(request, "El proyecto ha sido actualizado y los cambios han sido registrados.")
            else:
                messages.info(request, "No hubo cambios en el proyecto.")
            
            return redirect('proyecto_detalle', proyecto_id=proyecto.id)
    else:
        form = ProyectoForm(instance=proyecto)

    return render(request, 'proyectos/actualizar.html', {'form': form})