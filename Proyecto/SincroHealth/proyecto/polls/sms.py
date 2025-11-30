from twilio.rest import Client
from django.conf import settings

def enviar_sms(numero_destino, mensaje):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=mensaje,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=numero_destino
        )

        print(f"SMS enviado a {numero_destino}. SID: {message.sid}")

    except Exception as e:
        print(f"Error enviando SMS a {numero_destino}: {str(e)}")
