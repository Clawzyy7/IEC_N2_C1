from presentacion.presentacion_base import PresentacionBase


class PresentacionEstado(PresentacionBase):
    TITULO = "Estados de cita"
    COLUMNAS = ["ID", "Estado", "Descripción"]
    CAMPOS = [("nombre", "Nombre del estado"), ("descripcion", "Descripción (opcional)")]

    def _fila(self, e):
        return [e.id_estado, e.nombre, e.descripcion]

    def _extras(self):
        return [("Cambiar estado (habilitar / deshabilitar)", self._cambiar_estado)]

    def _cambiar_estado(self):
        id_ = self._pedir_entero("Id del estado")
        habilitar = self._pedir_texto("1 = habilitar, 0 = deshabilitar") == "1"
        self._negocio.cambiar_estado(id_, habilitar)
        print("✔ Estado actualizado.")
