from auxiliares.formato import fecha_hora_a_texto
from presentacion.presentacion_base import PresentacionBase


class PresentacionHistorial(PresentacionBase):
    TITULO = "Historial clínico"
    COLUMNAS = ["ID", "Ficha", "Paciente", "Cita", "Motivo", "Diagnóstico", "Tratamiento",
                "Obs.", "Actualizado"]
    CAMPOS = [("motivo", "Motivo"), ("diagnostico", "Diagnóstico (opcional)"),
              ("tratamiento", "Tratamiento (opcional)"), ("observaciones", "Observaciones (opcional)")]

    def _fila(self, h):
        return [h.id_historial, h.__data__.get("ficha"), h.__data__.get("paciente"),
                h.__data__.get("cita"), h.motivo, h.diagnostico, h.tratamiento,
                h.observaciones, fecha_hora_a_texto(h.fecha_actualizacion)]

    def _agregar(self):
        """Usa registrar_historial(): el paciente se toma de la ficha."""
        id_ficha = self._pedir_entero("Id de la ficha")
        id_cita = self._pedir_entero("Id de la cita")
        motivo = self._pedir_texto("Motivo")
        diagnostico = self._pedir_texto("Diagnóstico (opcional)")
        tratamiento = self._pedir_texto("Tratamiento (opcional)")
        observaciones = self._pedir_texto("Observaciones (opcional)")
        historial = self._negocio.registrar_historial(id_ficha, id_cita, motivo, diagnostico,
                                                      tratamiento, observaciones)
        print(f"✔ Historial registrado con id {historial.get_id()}.")
