from django.core.mail import send_mail
from django.conf import settings

def enviar_correo(destinatario, asunto, mensaje):
    try:
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[destinatario],
            fail_silently=False
        )

        print(f"Correo enviado a {destinatario}")

    except Exception as e:
        print(f"Error enviando correo a {destinatario}: {str(e)}")
