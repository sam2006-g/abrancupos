from django.shortcuts import render
from app_sujeto.models import Frase
from app_sujeto.sujeto import Sujeto

def mostrar_sujeto(request):
    frase = None
    if request.method == "POST":
        sujeto = Sujeto()
        primera_frase = Frase.objects.first()
        if primera_frase:
            sujeto.modificar_frase(primera_frase.texto)
            frase = sujeto.hablar()
    return render(request, "app_sujeto/index.html", {"frase": frase})
