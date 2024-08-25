from django.http import HttpResponse
<<<<<<< HEAD
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



def login(request):
    return render(request, 'login.html')

def registro(request):
    return render(request, 'registro.html')

@login_required
def vista(request):
=======
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import User
from django.contrib import messages
#from django.contrib.auth.hashers import make_password


#----------------Inicio----------------
def home(request):
    return render(request, 'index.html')
#----------------Vista de proyectos----------------
@login_required
def projectos(request):
>>>>>>> proyectos
    return render(request,'vistaprojectos.html')
#----------------Actualizar perfil----------------

<<<<<<< HEAD
def actualizar_perfil(request):
    return render(request,'perfilconfig.html')

def perfilconfig(request):
    return render(request,'perfilconfig.html')
=======
@login_required
def actualizarperfil(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        number_phone = request.POST.get('number_phone')
        location = request.POST.get('location')
        password = request.POST.get('password')
>>>>>>> proyectos

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
