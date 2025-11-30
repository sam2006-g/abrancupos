from datetime import date, timedelta
from polls.models import CitaMedica
from polls.sms import enviar_sms
from polls.email_utils import enviar_correo

def enviar_notificaciones():
    hoy = date.today()

    recordatorios = {
        "dentro de 1 semana": hoy + timedelta(days=7),
        "dentro de 3 días": hoy + timedelta(days=3),
        "el día de mañana": hoy + timedelta(days=1),
        "el día de hoy": hoy,
    }

    for tipo, fecha_objetivo in recordatorios.items():
        print(f"\n Buscando citas para {tipo} ({fecha_objetivo})...")

        citas = CitaMedica.objects.filter(fecha=fecha_objetivo)

        for cita in citas:
            paciente = cita.idpaciente
            telefono = f"+57{paciente.telefono}"  
            
            mensaje_email = (
                f"Hola {paciente.nombre},\n\n"
                f"Este es un recordatorio: tienes una cita médica "
                f"{tipo}.\n\n"
                f"Fecha: {cita.fecha}\n"
                f"Hora: {cita.hora}\n"
                f"Médico: {cita.idmedico}\n\n"
                "SincroHealth"
            )

            enviar_correo(
                destinatario=paciente.correo_electronico,
                asunto="Recordatorio de cita médica",
                mensaje=mensaje_email
            )

            mensaje_sms = (
                f"Recordatorio SincroHealth: cita {tipo}. "
                f"{cita.fecha} a las {cita.hora}."
            )

            enviar_sms(
                numero_destino=telefono,
                mensaje=mensaje_sms
            )

            print(f"Notificación enviada a {paciente.nombre} ({tipo})")
