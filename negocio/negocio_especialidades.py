from datos.modelos.especialidad import Especialidad
from auxiliares.validaciones import v_texto
from negocio.negocio_base import NegocioBase


class NegocioEspecialidades(NegocioBase):
    MODELO = Especialidad
    NOMBRE = "la especialidad"
    CAMPOS = {
        "nombre": v_texto("El nombre", 80),
        "descripcion": v_texto("La descripción", 200, obligatorio=False),
    }

    def _reglas(self, objeto):
        self._exigir_unico(objeto, self._repo.buscar_por_nombre(objeto.nombre),
                           "el nombre", objeto.nombre)
