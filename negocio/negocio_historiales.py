from datetime import datetime

from auxiliares.excepciones import ValidacionError
from auxiliares.validaciones import v_entero, v_texto
from datos.modelos.historial_clinica import HistorialClinica
from negocio.negocio_base import NegocioBase


class NegocioHistoriales(NegocioBase):
    MODELO = HistorialClinica
    NOMBRE = "el historial"
    CAMPOS = {
        "ficha": v_entero("El id de la ficha"),
        "paciente": v_entero("El id del paciente"),
        "cita": v_entero("El id de la cita"),
        "motivo": v_texto("El motivo", 255),
        "diagnostico": v_texto("El diagnóstico", 500, obligatorio=False),
        "tratamiento": v_texto("El tratamiento", 500, obligatorio=False),
        "observaciones": v_texto("Las observaciones", 255, obligatorio=False),
    }

    def __init__(self, repo_historial, repo_ficha, repo_cita):
        super().__init__(repo_historial)
        self._fichas = repo_ficha
        self._citas = repo_cita

    def _reglas(self, objeto):
        """El historial se valida contra su ficha y su cita."""
        id_paciente = self._id_de(objeto, "paciente")
        ficha = self._fichas.obtener_por_id(self._id_de(objeto, "ficha"))
        if ficha is None:
            raise ValidacionError(f"No existe la ficha con id {self._id_de(objeto, 'ficha')}.")
        if ficha.__data__.get("paciente") != id_paciente:
            raise ValidacionError(f"La ficha {ficha.get_id()} pertenece a otro paciente.")
        cita = self._citas.obtener_por_id(self._id_de(objeto, "cita"))
        if cita is None:
            raise ValidacionError(f"No existe la cita con id {self._id_de(objeto, 'cita')}.")
        if cita.__data__.get("paciente") != id_paciente:
            raise ValidacionError(f"La cita {cita.get_id()} no pertenece a ese paciente.")
        objeto.fecha_actualizacion = datetime.now()

    def registrar_historial(self, id_ficha, id_cita, motivo, diagnostico="", tratamiento="",
                            observaciones=""):
        """El paciente se toma de la ficha, así no puede haber inconsistencias."""
        ficha = self._fichas.obtener_por_id(self.CAMPOS["ficha"](id_ficha))
        if ficha is None:
            raise ValidacionError(f"No existe la ficha con id {id_ficha}.")
        return self.agregar({
            "ficha": id_ficha, "paciente": ficha.__data__.get("paciente"), "cita": id_cita,
            "motivo": motivo, "diagnostico": diagnostico, "tratamiento": tratamiento,
            "observaciones": observaciones})

    def consultar_historial(self, id_historial):
        return self.obtener(id_historial)

    def modificar_historial(self, id_historial, datos):
        return self.modificar(id_historial, datos)
