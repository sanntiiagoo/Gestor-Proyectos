from django.http import HttpResponse
from django.shortcuts import render



def home(request):
    return render(request, 'index.html')

def projectosvista(request):
    return render(request,'vistaprojectos.html')

def actualizarperfil(request):
    return render(request,'perfilconfig.html')

#pa ver nomas el footer----------------
def footer(request):
    return render(request,'footer.html')
#------------------------------------------