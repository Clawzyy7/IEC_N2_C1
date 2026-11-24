from presentacion.presentacion_base import PresentacionBase


class PresentacionEspecialidad(PresentacionBase):
    TITULO = "Especialidades"
    COLUMNAS = ["ID", "Especialidad", "Descripción"]
    CAMPOS = [("nombre", "Nombre de la especialidad"),
              ("descripcion", "Descripción (opcional)")]

    def _fila(self, e):
        return [e.id_especialidad, e.nombre, e.descripcion]
