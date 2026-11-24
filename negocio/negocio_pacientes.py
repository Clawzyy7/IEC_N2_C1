from auxiliares.validaciones import validar_fecha_nacimiento
from datos.modelos.paciente import Paciente
from negocio.negocio_persona import NegocioPersona


class NegocioPacientes(NegocioPersona):
    MODELO = Paciente
    NOMBRE = "el paciente"
    CAMPOS = {**NegocioPersona.CAMPOS, "fecha_nacimiento": validar_fecha_nacimiento}

    def __init__(self, repo_paciente, repo_historial, negocio_citas):
        super().__init__(repo_paciente)
        self._historiales = repo_historial
        self._citas = negocio_citas

    def solicitar_cita(self, id_paciente, id_profesional, observaciones=""):
        return self._citas.reservar(id_paciente, id_profesional, observaciones)

    def consultar_historial(self, id_paciente):
        self.obtener(id_paciente)
        return self._historiales.listar_por_paciente(id_paciente)
