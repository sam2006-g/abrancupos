from django.urls import path
from . import views

urlpatterns = [
    path("paciente/<int:idpaciente>/citas/", views.citas_paciente, name="citas_paciente"),
    path("medico/<int:idmedico>/horario/", views.horario_medico, name="horario_medico"),
    path("paciente/<int:idpaciente>/historial/", views.vista_historial, name="historial_html"),
    path("paciente/<int:idpaciente>/historial/pdf/", views.historial_pdf, name="historial_pdf"),
]