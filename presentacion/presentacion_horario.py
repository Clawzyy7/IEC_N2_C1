from auxiliares.formato import fecha_a_texto, hora_a_texto
from presentacion.presentacion_base import PresentacionBase


class PresentacionHorario(PresentacionBase):
    TITULO = "Horarios de atención"
    COLUMNAS = ["ID", "Profesional", "Fecha", "Inicio", "Fin", "Bloque (min)", "Bloques"]
    CAMPOS_SOLO_CREAR = [("profesional", "Id del profesional")]
    CAMPOS = [("fecha", "Fecha (dd/mm/aaaa)"), ("hora_inicio", "Hora de inicio (HH:MM)"),
              ("hora_fin", "Hora de fin (HH:MM)"),
              ("duracion_bloque", "Duración de cada bloque (minutos)")]

    def _fila(self, h):
        return [h.id_horario, h.profesional.nombre_completo, fecha_a_texto(h.fecha),
                hora_a_texto(h.hora_inicio), hora_a_texto(h.hora_fin), h.duracion_bloque,
                h.cantidad_bloques]
