from django.contrib import admin
from .models import Paciente, Medico, Administrador, CitaMedica, RecetaMedica, HistorialMedico

admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Administrador)
admin.site.register(CitaMedica)
admin.site.register(RecetaMedica)
admin.site.register(HistorialMedico)
