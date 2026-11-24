from datetime import date

from auxiliares.excepciones import ValidacionError
from auxiliares.formato import a_hora, fecha_a_texto, hora_a_texto
from auxiliares.validaciones import v_entero, v_fecha, v_hora
from datos.modelos.horario_atencion import HorarioAtencion
from negocio.negocio_base import NegocioBase


class NegocioHorarios(NegocioBase):
    MODELO = HorarioAtencion
    NOMBRE = "la jornada"
    CAMPOS = {
        "profesional": v_entero("El id del profesional"),
        "fecha": v_fecha("La fecha"),
        "hora_inicio": v_hora("La hora de inicio"),
        "hora_fin": v_hora("La hora de fin"),
        "duracion_bloque": v_entero("La duración del bloque (minutos)", 5, 240),
    }

    def __init__(self, repo_horario, repo_profesional):
        super().__init__(repo_horario)
        self._profesionales = repo_profesional

    def _reglas(self, objeto):
        id_profesional = self._id_de(objeto, "profesional")
        self._exigir_activo(self._profesionales, id_profesional, "el profesional")
        inicio, fin = a_hora(objeto.hora_inicio), a_hora(objeto.hora_fin)
        if fin <= inicio:
            raise ValidacionError("La hora de fin debe ser posterior a la hora de inicio.")
        if objeto.duracion_bloque > objeto.minutos_jornada:
            raise ValidacionError("La duración del bloque es mayor que la jornada.")
        if objeto.get_id() is None and objeto.fecha < date.today():
            raise ValidacionError("No se puede registrar una jornada en una fecha pasada.")
        # Regla: un profesional no puede tener dos jornadas que se solapen el mismo día
        for otra in self._repo.listar_por_profesional_fecha(id_profesional, objeto.fecha):
            if otra.get_id() != objeto.get_id() and inicio < a_hora(otra.hora_fin) \
                    and a_hora(otra.hora_inicio) < fin:
                raise ValidacionError(
                    f"Se solapa con la jornada {otra.get_id()} "
                    f"({fecha_a_texto(otra.fecha)} {hora_a_texto(otra.hora_inicio)}-"
                    f"{hora_a_texto(otra.hora_fin)}).")

    def registrar_jornada(self, datos):
        return self.agregar(datos)

    def modificar_jornada(self, id_horario, datos):
        return self.modificar(id_horario, datos)
