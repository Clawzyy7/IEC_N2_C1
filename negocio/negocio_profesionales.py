from datetime import date

from auxiliares.excepciones import ValidacionError
from auxiliares.validaciones import v_entero
from datos.modelos.profesional import Profesional
from negocio.negocio_persona import NegocioPersona


class NegocioProfesionales(NegocioPersona):
    MODELO = Profesional
    NOMBRE = "el profesional"
    CAMPOS = {**NegocioPersona.CAMPOS, "especialidad": v_entero("El id de la especialidad")}

    def __init__(self, repo_profesional, repo_especialidad, repo_horario, negocio_citas):
        super().__init__(repo_profesional)
        self._especialidades = repo_especialidad
        self._horarios = repo_horario
        self._citas = negocio_citas

    # Polimorfismo: sobrescritura (agrega la regla de la especialidad a la de la persona)
    def _reglas(self, objeto):
        super()._reglas(objeto)
        self._exigir_activo(self._especialidades, self._id_de(objeto, "especialidad"),
                            "la especialidad")

    def consultar_agenda(self, id_profesional):
        """Jornadas vigentes y citas del profesional."""
        return {
            "profesional": self.obtener(id_profesional),
            "jornadas": self._horarios.listar_por_profesional(id_profesional),
            "citas": self._citas.listar_citas(id_profesional=id_profesional),
        }

    def agendar_hora(self, id_profesional, id_paciente, observaciones=""):
        """Reserva una cita con el profesional, siempre que tenga jornadas vigentes."""
        self._exigir_activo(self._repo, id_profesional, "el profesional")
        jornadas = self._horarios.listar_por_profesional(id_profesional)
        if not any(j.fecha >= date.today() for j in jornadas):
            raise ValidacionError("El profesional no tiene jornadas vigentes registradas.")
        return self._citas.reservar(id_paciente, id_profesional, observaciones)
