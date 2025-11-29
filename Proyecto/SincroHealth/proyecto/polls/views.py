from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import CitaMedica, Paciente, Medico, HistorialMedico
from datetime import date, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def citas_paciente(request, idpaciente):
    paciente = Paciente.objects.get(idpaciente=idpaciente)
    citas = CitaMedica.objects.filter(idpaciente=paciente)
    
    return render(request, "citas/lista_citas.html", {
        "paciente":paciente,
        "citas":citas
    })
def crear_cita(request):
    if request.method == "POST":
        pass

    return render(request, "citas/crear_cita.html")

def horario_medico(request,idmedico):
    medico = Medico.objects.get(idmedico=idmedico)
    hoy = date.today()
    lunes = hoy - timedelta(days=hoy.weekday())        
    domingo = lunes + timedelta(days=6)  
    citas_semana = CitaMedica.objects.filter(
        idmedico=medico,
        fecha__range=[lunes, domingo]
    ).order_by("fecha", "hora")
    dias = {}
    for i in range(7):
        dia = lunes + timedelta(days=i)
        dias[dia] = []
    for cita in citas_semana:
        dias[cita.fecha].append(cita)
    return render(request, "citas/horario_medico.html", {
        "medico": medico,
        "dias":dias,
        "lunes":lunes,
        "domingo":domingo
    })

def vista_historial(request, idpaciente):
    paciente = get_object_or_404(Paciente, idpaciente=idpaciente)
    historial = get_object_or_404(HistorialMedico, idpaciente=paciente)
    return render(request, "historial/historial.html", {
        "paciente": paciente,
        "historial": historial,
    })

def historial_pdf(request, idpaciente):

    paciente = Paciente.objects.get(pk=idpaciente)
    historial, creado = HistorialMedico.objects.get_or_create(idpaciente=paciente)

    response = HttpResponse(content_type="application/pdf")
    response["X-Frame-Options"] = "ALLOWALL"
    response["X-Content-Type-Options"] = "nosniff"
    if request.GET.get("preview") == "1":
        response["Content-Disposition"] = "inline; filename=historial.pdf"
    else:
        response["Content-Disposition"] = f'attachment; filename="historial_{paciente.idpaciente}.pdf"'
        
    p = canvas.Canvas(response, pagesize=letter)
    y = 750
    p.setTitle(f"{paciente.nombre} {paciente.apellidos}")
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Historial Médico")
    y -= 30

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Paciente: {paciente.nombre} {paciente.apellidos}")
    y -= 20

    p.drawString(50, y, f"Fecha: {historial.fecha}")
    y -= 40

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Recetas registradas:")
    y -= 25

    p.setFont("Helvetica", 12)
    if not historial.recetas_json:
        p.drawString(50, y, "No hay recetas registradas.")
    else:
        for receta in historial.recetas_json:
            text = (
                f"- ({receta['idrecetas_medicas']}) "
                f"{receta['diagnostico']} | "
                f"{receta['medicamentos']} ({receta['indicaciones']})"
            )
            p.drawString(50, y, text)
            y -= 20
            if y < 50:
                p.showPage()
                y = 750

    p.showPage()
    p.save()

    return response

