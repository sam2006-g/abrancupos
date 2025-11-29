from datetime import date, timedelta
from django.core.mail import send_mail
from django.conf import settings
from polls.models import CitaMedica


def enviar_notificaciones():
    hoy = date.today()

    dias_alertas = {
        7: "Falta 1 semana",
        3: "Faltan 3 días",
        1: "Falta 1 día",
        0: "preparate hoy"     
    }

    for dias, mensaje_alerta in dias_alertas.items():
        fecha_objetivo = hoy + timedelta(days=dias)
        citas = CitaMedica.objects.filter(fecha=fecha_objetivo)

        for cita in citas:
            paciente = cita.idpaciente

            mensaje = (
                f"Hola {paciente.nombre},\n\n"
                f"{mensaje_alerta} para tu cita médica.\n"
                f"Fecha: {cita.fecha}\n"
                f"Hora: {cita.hora}\n"
                f"Especialidad: {cita.especialidad}\n\n"
                "Te esperamos."
            )

            send_mail(
                subject=f"Recordatorio de cita — {mensaje_alerta}",
                message=mensaje,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[paciente.correo_electronico],
                fail_silently=False,
            )

            print(f"Correo ({mensaje_alerta}) enviado a: {paciente.correo_electronico}")
