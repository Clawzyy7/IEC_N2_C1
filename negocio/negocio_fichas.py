from auxiliares.excepciones import ValidacionError
from auxiliares.validaciones import v_entero, v_texto
from datos.modelos.ficha_paciente import FichaPaciente
from negocio.negocio_base import NegocioBase


class NegocioFichas(NegocioBase):
    MODELO = FichaPaciente
    NOMBRE = "la ficha"
    CAMPOS = {
        "paciente": v_entero("El id del paciente"),
        "motivo": v_texto("El motivo", 255),
        "diagnostico": v_texto("El diagnóstico", 500, obligatorio=False),
        "tratamiento": v_texto("El tratamiento", 500, obligatorio=False),
    }

    def __init__(self, repo_ficha, repo_paciente):
        super().__init__(repo_ficha)
        self._pacientes = repo_paciente

    def _reglas(self, objeto):
        id_paciente = self._id_de(objeto, "paciente")
        self._exigir_activo(self._pacientes, id_paciente, "el paciente")
        # Relación 1:1: un paciente tiene una sola ficha
        existente = self._repo.buscar_por_paciente(id_paciente)
        if existente is not None and existente.get_id() != objeto.get_id():
            raise ValidacionError(f"El paciente {id_paciente} ya tiene la ficha "
                                  f"{existente.get_id()}.")

    def consultar_ficha(self, id_paciente):
        ficha = self._repo.buscar_por_paciente(id_paciente)
        if ficha is None:
            raise ValidacionError(f"El paciente {id_paciente} no tiene ficha.")
        return ficha

    def modificar_ficha(self, id_ficha, datos):
        return self.modificar(id_ficha, datos)

    def anular_ficha(self, id_ficha):
        """Borrado real. Falla si la ficha ya tiene historial clínico asociado."""
        self.eliminar(id_ficha)
