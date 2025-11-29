from app_sujeto.models import Frase

class Sujeto:
    def __init__(self):
        self.frase = ""

    def modificar_frase(self, nueva_frase):
        self.frase = nueva_frase

    def hablar(self):
        return self.frase
