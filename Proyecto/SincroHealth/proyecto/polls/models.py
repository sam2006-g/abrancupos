from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
)
password_validator = RegexValidator(
    regex=r'^[A-Za-z0-9!@#$%^&*()_\-+=\[\]{};:,.<>?/|~`]{5,25}$',
    message="La contraseña debe tener entre 5 y 25 caracteres; esta puede contener letras, números y caracteres especiales."
)
hora_validator = RegexValidator(
    regex=r'^(?:[01]\d|2[0-3]):[0-5]\d$',
    message="La hora debe estar en formato HH:MM."
)


class Paciente(models.Model):
    idpaciente = models.IntegerField(primary_key=True)
    contrasena = models.CharField(max_length=25, validators=[password_validator])
    nombre = models.CharField(max_length=45, validators=[MinLengthValidator(2)])
    apellidos = models.CharField(max_length=45, validators=[MinLengthValidator(2)])
    direccion = models.CharField(max_length=45)
    correo_electronico = models.EmailField(max_length=45)
    telefono = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Medico(models.Model):
    idmedico = models.IntegerField(primary_key=True)
    contrasena = models.CharField(max_length=25, validators=[password_validator])
    nombre = models.CharField(max_length=45, validators=[MinLengthValidator(2)])
    apellidos = models.CharField(max_length=45, validators=[MinLengthValidator(2)])
    especialidad = models.CharField(max_length=45, validators=[MinLengthValidator(2)])
    correo_electronico = models.EmailField(max_length=45)
    telefono = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} {self.apellidos} | Especialidad: {self.especialidad}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Administrador(models.Model):
    idadministradores = models.OneToOneField(User, on_delete=models.CASCADE)
    contraseña = models.CharField(max_length=25, validators=[password_validator])
    nombre = models.CharField(max_length=45, validators=[MinLengthValidator(2)])
    apellidos = models.CharField(max_length=45, validators=[MinLengthValidator(2)])
    correo_electronico = models.EmailField(max_length=45)
    telefono = models.IntegerField()

    def __str__(self):
        return f"{self.idadministradores.username} | Nombre: {self.nombre}{self.apellidos}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class CitaMedica(models.Model):
    idcitas_medicas = models.AutoField(primary_key=True)
    idpaciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    idmedico = models.ForeignKey('Medico', on_delete=models.CASCADE, null=True, blank=True)
    especialidad = models.CharField(max_length=45)
    fecha = models.DateField()
    hora = models.CharField(max_length=45, validators=[hora_validator])
    ESTADOS = [("Pendiente", "Pendiente"), ("Cancelada", "Cancelada"), ("Confirmada", "Confirmada")]
    estado_cita = models.CharField(max_length=45, choices=ESTADOS, default="Pendiente")

    def __str__(self):
        medico = f"{self.idmedico.nombre} {self.idmedico.apellidos}" if self.idmedico else "Sin asignar"
        return (
            f"{self.idcitas_medicas} | Especialidad: {self.especialidad} | "
            f"Médico: {medico} | Paciente: {self.idpaciente.nombre} {self.idpaciente.apellidos} | "
            f"Fecha: {self.fecha} | Hora: {self.hora}"
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class RecetaMedica(models.Model):
    idrecetas_medicas = models.AutoField(primary_key=True)
    idpaciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    idmedico = models.ForeignKey('Medico', on_delete=models.CASCADE, null=True, blank=True)
    idcitas_medicas = models.ForeignKey('CitaMedica', on_delete=models.CASCADE)
    diagnostico = models.CharField(max_length=300, validators=[MinLengthValidator(2)])
    medicamentos = models.CharField(max_length=45)
    indicaciones = models.CharField(max_length=45)

    def __str__(self):
        return (
            f"{self.idrecetas_medicas} | "
            f"Paciente: {self.idpaciente.nombre} {self.idpaciente.apellidos} | "
            f"Médico: {self.idmedico.nombre} {self.idmedico.apellidos} | "
            f"Cita: {self.idcitas_medicas.idcitas_medicas}"
        )

    def clean(self):
        super(RecetaMedica, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class HistorialMedico(models.Model):
    idhistorial = models.AutoField(primary_key=True)
    idpaciente = models.OneToOneField('Paciente', on_delete=models.CASCADE)
    recetas_json = models.JSONField(blank=True, default=list)
    fecha = models.DateField(auto_now=True)

    def actualizar_recetas(self):
        recetas = self.idpaciente.recetamedica_set.all().values(
            'idrecetas_medicas',
            'diagnostico',
            'medicamentos',
            'indicaciones',
            'idcitas_medicas'
        )
        self.recetas_json = list(recetas)
        self.save(update_fields=["recetas_json"])

    def __str__(self):
        recetas_texto = "; ".join(
            [f"(ID {r['idrecetas_medicas']}) {r['diagnostico']} - {r['medicamentos']} ({r['indicaciones']})"
             for r in self.recetas_json]
        ) if self.recetas_json else "Sin recetas registradas"
        return (
            f"Historial del paciente {self.idpaciente.nombre}"
            f"{self.idpaciente.apellidos} - {self.fecha} | "
            f"Recetas: {recetas_texto}"
        )


@receiver(post_save, sender='polls.RecetaMedica')
def actualizar_historial_al_guardar(sender, instance, **kwargs):
    paciente = instance.idpaciente
    historial, creado = HistorialMedico.objects.get_or_create(idpaciente=paciente)
    historial.actualizar_recetas()


@receiver(post_delete, sender='polls.RecetaMedica')
def actualizar_historial_al_eliminar(sender, instance, **kwargs):
    paciente = instance.idpaciente
    historial = HistorialMedico.objects.filter(idpaciente=paciente).first()
    if historial:
        historial.actualizar_recetas()


class Auditoria(models.Model):
    idauditoria = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    fecha = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.idauditoria} - {self.descripcion}"
