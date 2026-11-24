from auxiliares.validaciones import v_texto
from datos.modelos.estado import Estado
from negocio.negocio_base import NegocioBase


class NegocioEstados(NegocioBase):
    MODELO = Estado
    NOMBRE = "el estado"
    CAMPOS = {
        "nombre": v_texto("El nombre", 80),
        "descripcion": v_texto("La descripción", 200, obligatorio=False),
    }

    def _reglas(self, objeto):
        self._exigir_unico(objeto, self._repo.buscar_por_nombre(objeto.nombre),
                           "el nombre", objeto.nombre)

    def obtener_estado(self, id_estado):
        return self.obtener(id_estado)

    def cambiar_estado(self, id_estado, habilitado):
        """Habilita o deshabilita un estado del catálogo."""
        estado = self.obtener(id_estado)
        estado.habilitado = bool(habilitado)
        return self._repo.guardar(estado)
