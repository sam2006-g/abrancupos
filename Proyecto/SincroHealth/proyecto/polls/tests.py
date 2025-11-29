from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import (
    Paciente, Medico, Administrador,
    CitaMedica, RecetaMedica, HistorialMedico
)
# TEST 01 — Crear paciente


class Test01_Crearpaciente(TestCase):
    def test_crear_paciente(self):
        # Caso Normal
        paciente1 = Paciente(
            idpaciente=1,
            contrasena="Abc12!",
            nombre="Juan",
            apellidos="perez",
            direccion="Calle 1",
            correo_electronico="jp@gmaigmail.com",
            telefono=123
        )
        paciente1.full_clean()
        paciente1.save()

        # Caso Límite Válido
        paciente2 = Paciente(
            idpaciente=2,
            contrasena="Aa1!!",
            nombre="Lu",
            apellidos="Ro",
            direccion="A",
            correo_electronico="x@gmaigmail.com",
            telefono=1
        )
        paciente2.full_clean()

        # Caso Límite Inválido
        paciente3 = Paciente(
            idpaciente=3,
            contrasena="A12!",
            nombre="Ana",
            apellidos="Gomez",
            direccion="X",
            correo_electronico="a@gnmaigmail.com",
            telefono=111,
        )
        with self.assertRaises(ValidationError):
            paciente3.full_clean()
# TEST 02 — Crear Médico


class Test02_CrearMedico(TestCase):
    def test_crear_medico(self):
        # Caso Normal
        medico1 = Medico(
            idmedico=10,
            contrasena="Fed12!",
            nombre="Ana",
            apellidos="Carvajal",
            especialidad="Cardiologia",
            correo_electronico="ana@gmaigmail.com",
            telefono=123
        )
        medico1.full_clean()
        medico1.save()

        # Caso Limite Valido
        medico2 = Medico(
            idmedico=11,
            contrasena="Aa1!!",
            nombre="Lu",
            apellidos="Ro",
            especialidad="AB",
            correo_electronico="b@gmaigmail.com",
            telefono=111
        )
        medico2.full_clean()

        # Caso Limite Invalido
        medico3 = Medico(
            idmedico=12,
            contrasena="Abc12!",
            nombre="Lu",
            apellidos="Ro",
            especialidad="A",
            correo_electronico="c@gmaigmail.com",
            telefono=222
        )
        with self.assertRaises(ValidationError):
            medico3.full_clean()
# TEST 03 — Crear Administrador


class Test03_CrearAdministrador(TestCase):
    def test_crear_admin(self):
        # Caso Normal
        user1 = User.objects.create(username="admin1")
        admin1 = Administrador(
            idadministradores=user1,
            contraseña="Admin12!",
            nombre="Carlos",
            apellidos="Lopez",
            correo_electronico="c@gmaigmail.com",
            telefono=123
        )
        admin1.full_clean()
        admin1.save()

        # Caso Limite Valido
        user2 = User.objects.create(username="admin2")
        admin2 = Administrador(
            idadministradores=user2,
            contraseña="A" * 25,
            nombre="Sa",
            apellidos="pe",
            correo_electronico="x@gmaigmail.com",
            telefono=111
        )
        admin2.full_clean()

        # Caso Limite Invalido
        user3 = User.objects.create(username="admin3")
        admin3 = Administrador(
            idadministradores=user3,
            contraseña="a" * 26,
            nombre="Lu",
            apellidos="Ro",
            correo_electronico="l@gmaigmail.com",
            telefono=123
        )
        with self.assertRaises(ValidationError):
            admin3.full_clean()
#  TEST 04 — Crear Cita Médica


class Test04_CrearCita(TestCase):
    def setUp(self):
        self.paciente1 = Paciente.objects.create(
            idpaciente=50, contrasena="Abc12!",
            nombre="pedro", apellidos="Mora",
            direccion="X", correo_electronico="p@gmaigmail.com",
            telefono=1
        )
        self.medico = Medico.objects.create(
            idmedico=60, contrasena="Abc12!",
            nombre="Mario", apellidos="Gil",
            especialidad="Dermatologia",
            correo_electronico="m@gmaigmail.com",
            telefono=5
        )

    def test_crear_cita(self):
        # Caso Normal
        cita1 = CitaMedica(
            idpaciente=self.paciente1,
            idmedico=self.medico,
            especialidad="Dermatologia",
            fecha=date.today(),
            hora="08:00"
        )
        cita1.full_clean()
        cita1.save()

        # Caso Limite Valido
        cita2 = CitaMedica(
            idpaciente=self.paciente1,
            idmedico=self.medico,
            especialidad="General",
            fecha=date.today(),
            hora="23:59"
        )
        cita2.full_clean()

        # Caso Limite Invalido
        cita3 = CitaMedica(
            idpaciente=self.paciente1,
            idmedico=self.medico,
            especialidad="General",
            fecha=date.today(),
            hora="8AM"
        )
        with self.assertRaises(ValidationError):
            cita3.full_clean()
#  TEST 05 — Cancelar Cita Médica


class Test05_CancelarCita(TestCase):
    def setUp(self):
        self.paciente1 = Paciente.objects.create(
            idpaciente=1000, contrasena="Abc12!",
            nombre="Luis", apellidos="Diaz",
            direccion="Z", correo_electronico="l@gmail.com",
            telefono=55
        )
        self.medico = Medico.objects.create(
            idmedico=1001, contrasena="Abc12!",
            nombre="Jorge", apellidos="Rios",
            especialidad="General",
            correo_electronico="j@j.com",
            telefono=99
        )

    def test_cancelar_cita(self):
        cita = CitaMedica.objects.create(
            idpaciente=self.paciente1,
            idmedico=self.medico,
            especialidad="General",
            fecha=date.today(),
            hora="09:00"
        )

        # Caso Normal
        cita.estado_cita = "Cancelada"
        cita.full_clean()
        cita.save()
        self.assertEqual(cita.estado_cita, "Cancelada")

        # Caso Limite Valido
        cita.estado_cita = "Cancelada"
        cita.full_clean()

        # Caso Limite Invalido
        cita.estado_cita = "XYZ"
        with self.assertRaises(ValidationError):
            cita.full_clean()
#  TEST 06 — Reprogramar Cita


class Test06_ReprogramarCita(TestCase):
    def setUp(self):
        self.paciente1 = Paciente.objects.create(
            idpaciente=2000, contrasena="Abc12!",
            nombre="Ana", apellidos="Lara",
            direccion="C", correo_electronico="a@a.com",
            telefono=33
        )
        self.medico = Medico.objects.create(
            idmedico=2001, contrasena="Abc12!",
            nombre="paula", apellidos="Soto",
            especialidad="General",
            correo_electronico="p@p.com",
            telefono=40
        )
        self.cita = CitaMedica.objects.create(
            idpaciente=self.paciente1,
            idmedico=self.medico,
            especialidad="General",
            fecha=date.today(),
            hora="10:00"
        )

    def test_reprogramar_cita(self):
        # Caso Normal
        nueva_fecha = date.today() + timedelta(days=3)
        self.cita.fecha = nueva_fecha
        self.cita.hora = "11:30"
        self.cita.full_clean()
        self.cita.save()

        # Caso Limite Valido
        self.cita.fecha = date.today() + timedelta(days=1)
        self.cita.hora = "23:59"
        self.cita.full_clean()

        # Caso Limite Invalido
        self.cita.hora = "11AM"
        with self.assertRaises(ValidationError):
            self.cita.full_clean()
#  TEST 07 — Confirmar Cita Médica


class Test07_ConfirmarCita(TestCase):
    def setUp(self):
        self.paciente1 = Paciente.objects.create(
            idpaciente=3000, contrasena="Abc12!",
            nombre="Sofia", apellidos="Mora",
            direccion="D", correo_electronico="s@s.com",
            telefono=44
        )
        self.medico = Medico.objects.create(
            idmedico=3001, contrasena="Abc12!",
            nombre="Raul", apellidos="Vega",
            especialidad="General",
            correo_electronico="r@r.com",
            telefono=88
        )

    def test_confirmar_cita(self):
        cita = CitaMedica.objects.create(
            idpaciente=self.paciente1, idmedico=self.medico,
            especialidad="General",
            fecha=date.today(),
            hora="14:00"
        )

        # Caso Normal
        cita.estado_cita = "Confirmada"
        cita.full_clean()
        cita.save()
        self.assertEqual(cita.estado_cita, "Confirmada")

        # Caso Límite válido
        cita.estado_cita = "Confirmada"
        cita.full_clean()

        # Caso Límite inválido
        cita.estado_cita = "XYZ"
        with self.assertRaises(ValidationError):
            cita.full_clean()
# TEST 08 — Crear Receta actualiza Historial


class Test08_RecetaCreaHistorial(TestCase):
    def setUp(self):
        self.paciente1 = Paciente.objects.create(
            idpaciente=4000, contrasena="Abc12!",
            nombre="Elena", apellidos="Ramos",
            direccion="A", correo_electronico="e@e.com",
            telefono=11
        )
        self.medico = Medico.objects.create(
            idmedico=4001, contrasena="Abc12!",
            nombre="Mario", apellidos="Zapata",
            especialidad="General",
            correo_electronico="m@m.com",
            telefono=22
        )
        self.cita = CitaMedica.objects.create(
            idpaciente=self.paciente1, idmedico=self.medico,
            especialidad="General",
            fecha=date.today(),
            hora="08:00"
        )

    def test_crear_receta_actualiza_historial(self):
        # Caso Normal
        receta1 = RecetaMedica(
            idpaciente=self.paciente1, idmedico=self.medico,
            idcitas_medicas=self.cita,
            diagnostico="Dolor fuerte",
            medicamentos="Ibuprofeno",
            indicaciones="Cada 8 horas"
        )
        receta1.full_clean()
        receta1.save()
        self.assertTrue(
            HistorialMedico.objects.filter(idpaciente=self.paciente1).exists()
        )

        # Caso Límite válido
        receta2 = RecetaMedica(
            idpaciente=self.paciente1, idmedico=self.medico,
            idcitas_medicas=self.cita,
            diagnostico="ABCDE",
            medicamentos="Med",
            indicaciones="Ind"
        )
        receta2.full_clean()

        # Caso Límite inválido
        receta3 = RecetaMedica(
            idpaciente=self.paciente1, idmedico=self.medico,
            idcitas_medicas=self.cita,
            diagnostico="B",
            medicamentos="Med",
            indicaciones="Ind"
        )
        with self.assertRaises(ValidationError):
            receta3.full_clean()
#  TEST 09 — Actualizar historial al agregar receta


class Test09_HistorialAgregaReceta(TestCase):
    def setUp(self):
        self.paciente1 = Paciente.objects.create(
            idpaciente=5000, contrasena="Abc12!",
            nombre="Daniel", apellidos="Lopez",
            direccion="G", correo_electronico="d@d.com",
            telefono=90
        )
        self.medico = Medico.objects.create(
            idmedico=5001, contrasena="Abc12!",
            nombre="Tomas", apellidos="Soto",
            especialidad="General",
            correo_electronico="t@t.com",
            telefono=66
        )
        self.cita = CitaMedica.objects.create(
            idpaciente=self.paciente1, idmedico=self.medico,
            especialidad="General",
            fecha=date.today(),
            hora="10:00"
        )

    def test_actualizar_al_agregar(self):
        # Caso Normal
        RecetaMedica.objects.create(
            idpaciente=self.paciente1, idmedico=self.medico,
            idcitas_medicas=self.cita,
            diagnostico="F1",
            medicamentos="Med1",
            indicaciones="I1"
        )
        historial = HistorialMedico.objects.get(idpaciente=self.paciente1)
        self.assertEqual(len(historial.recetas_json), 1)

        # Caso Límite válido
        RecetaMedica.objects.create(
            idpaciente=self.paciente1, idmedico=self.medico,
            idcitas_medicas=self.cita,
            diagnostico="ABCDE",
            medicamentos="Med",
            indicaciones="Ind"
        )
        historial.refresh_from_db()
        self.assertEqual(len(historial.recetas_json), 2)

        # Caso Límite inválido
        receta3 = RecetaMedica(
            idpaciente=self.paciente1, idmedico=self.medico,
            idcitas_medicas=self.cita,
            diagnostico="A",
            medicamentos="M",
            indicaciones="I"
        )
        with self.assertRaises(ValidationError):
            receta3.full_clean()
#  TEST 10 — Actualizar historial al eliminar receta


class Test10_HistorialEliminaReceta(TestCase):
    def setUp(self):
        self.paciente1 = Paciente.objects.create(
            idpaciente=6000, contrasena="Abc12!",
            nombre="Carla", apellidos="Rey",
            direccion="A", correo_electronico="c@c.com",
            telefono=33
        )
        self.medico = Medico.objects.create(
            idmedico=6001, contrasena="Abc12!",
            nombre="Jose", apellidos="Marin",
            especialidad="General",
            correo_electronico="j@j.com",
            telefono=44
        )
        self.cita = CitaMedica.objects.create(
            idpaciente=self.paciente1, idmedico=self.medico,
            especialidad="General",
            fecha=date.today(),
            hora="08:00"
        )

    def test_eliminar_receta_actualiza(self):
        # Caso Normal
        receta1 = RecetaMedica.objects.create(
            idpaciente=self.paciente1, idmedico=self.medico,
            idcitas_medicas=self.cita,
            diagnostico="Dolor tipo 1", medicamentos="A", indicaciones="B"
        )
        historial = HistorialMedico.objects.get(idpaciente=self.paciente1)
        self.assertEqual(len(historial.recetas_json), 1)
        receta1.refresh_from_db()
        receta1.delete()
        historial.refresh_from_db()
        self.assertEqual(len(historial.recetas_json), 0)
        # Caso Límite inválido
        with self.assertRaises(RecetaMedica.DoesNotExist):
            RecetaMedica.objects.get(idrecetas_medicas=9999)
#  TEST 11 — Eliminar Historial Médico


class Test11_EliminarHistorial(TestCase):
    def setUp(self):
        self.paciente1 = Paciente.objects.create(
            idpaciente=9000,
            contrasena="Abc12!",
            nombre="Mario",
            apellidos="Lopez",
            direccion="Calle X",
            correo_electronico="mario@gmaigmail.com",
            telefono=55
        )
        self.historial = HistorialMedico.objects.create(idpaciente=self.paciente1)

    def test_eliminar_historial(self):
        self.assertTrue(HistorialMedico.objects.filter(idpaciente=self.paciente1).exists())
        # Caso Normal
        self.historial.delete()
        self.assertFalse(HistorialMedico.objects.filter(idpaciente=self.paciente1).exists())
        # Caso Limite Valido
        self.assertTrue(Paciente.objects.filter(idpaciente=self.paciente1.idpaciente).exists())
        # Caso Limite Invalido
        with self.assertRaises(HistorialMedico.DoesNotExist):
            HistorialMedico.objects.get(idpaciente_id=99234).delete()
#  TEST 12 — Eliminar paciente Eliminar Información


class Test12_Eliminarpaciente(TestCase):
    def test_eliminar_paciente(self):
        # Caso Normal
        paciente1 = Paciente.objects.create(
            idpaciente=8000, contrasena="Abc12!",
            nombre="Eva", apellidos="Castro",
            direccion="A", correo_electronico="e@e.com",
            telefono=11
        )
        HistorialMedico.objects.create(idpaciente=paciente1)
        paciente1.delete()
        self.assertFalse(
            HistorialMedico.objects.filter(idpaciente=paciente1.idpaciente).exists()
        )

        # Caso Limite Valido: paciente sin historial
        paciente2 = Paciente.objects.create(
            idpaciente=8001, contrasena="Abc12!",
            nombre="Lu", apellidos="pe",
            direccion="C", correo_electronico="x@x.com",
            telefono=14
        )
        paciente2.delete()  # no debe fallar

        # Caso Limite Invalido: eliminar paciente inexistente
        with self.assertRaises(Paciente.DoesNotExist):
            Paciente.objects.get(idpaciente=959391)

