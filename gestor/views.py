from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



def login(request):
    return render(request, 'login.html')

def registro(request):
    return render(request, 'registro.html')

@login_required
def vista(request):
    return render(request,'vistaprojectos.html')

def actualizar_perfil(request):
    return render(request,'perfilconfig.html')

def perfilconfig(request):
    return render(request,'perfilconfig.html')

#pa ver nomas el footer----------------
def footer(request):
    return render(request,'footer.html')
#------------------------------------------