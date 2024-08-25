
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
#from django.contrib.auth.hashers import make_password


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
            return redirect('projectos')  # Redirige a la vista de proyectos si el login es exitoso
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')
    return render(request, 'login.html')

#----------------Registro----------------

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso. Por favor, elige otro.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado. Por favor, usa otro.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            auth_login(request, user)
            return redirect('home')  # Redirige a la vista 'home' después del registro exitoso
        
    return render(request, 'registro.html')
        
#----------------Vista de proyectos----------------
@login_required
def projectos(request):
    return render(request,'vistaprojectos.html')
#----------------Actualizar perfil----------------

@login_required
def actualizarperfil(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        number_phone = request.POST.get('number_phone')
        location = request.POST.get('location')
        password = request.POST.get('password')

        # Actualizar los campos del usuario
        user = request.user
        user.username = username
        user.email = email
        user.number_phone = number_phone
        user.location = location

        if password:
            user.set_password(password)

        user.save()

        messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
        return redirect('projectos')  # Redirige de vuelta a la página de perfil

    return render(request, 'perfilconfig.html')  # Asegúrate de que este nombre coincida con tu archivo de plantilla
