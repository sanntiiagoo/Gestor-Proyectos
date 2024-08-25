from django.http import HttpResponse
from django.shortcuts import render



def login(request):
    return render(request, 'login.html')

def registro(request):
    return render(request, 'registro.html')
def vista_projectos(request):
    return render(request,'vistaprojectos.html')

def actualizar_perfil(request):
    return render(request,'perfilconfig.html')

#pa ver nomas el footer----------------
def footer(request):
    return render(request,'footer.html')
#------------------------------------------