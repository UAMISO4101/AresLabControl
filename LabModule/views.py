from django.shortcuts import render


# Create your views here.
def home(request):
    context = {}

    return render(request, "home.html", context)


def agregar_lugar(request):
    return render(request, 'LugarAlmacenamiento/agregar.html')
