from presentacion.presentacion_base import PresentacionBase


class PresentacionFicha(PresentacionBase):
    TITULO = "Fichas de pacientes"
    COLUMNAS = ["ID", "Paciente", "Motivo", "Diagnóstico", "Tratamiento"]
    ETIQUETA_ELIMINAR = "Anular ficha"
    CAMPOS_SOLO_CREAR = [("paciente", "Id del paciente")]
    CAMPOS = [("motivo", "Motivo de consulta"), ("diagnostico", "Diagnóstico (opcional)"),
              ("tratamiento", "Tratamiento (opcional)")]

    def _fila(self, f):
        return [f.id_ficha, f.paciente.nombre_completo, f.motivo, f.diagnostico, f.tratamiento]

    def _eliminar(self):
        self._listar()
        self._negocio.anular_ficha(self._pedir_entero("Id de la ficha a anular"))
        print("✔ Ficha anulada.")

    def _extras(self):
        return [("Consultar ficha de un paciente", self._consultar_ficha)]

    def _consultar_ficha(self):
        self._mostrar_tabla([self._negocio.consultar_ficha(self._pedir_entero("Id del paciente"))])
