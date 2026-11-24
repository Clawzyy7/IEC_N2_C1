"""NegocioPersona: reglas y campos comunes de Paciente y Profesional (herencia)."""
from auxiliares.excepciones import ValidacionError
from auxiliares.validaciones import v_texto, validar_email, validar_rut, validar_telefono
from negocio.negocio_base import NegocioBase


class NegocioPersona(NegocioBase):
    CAMPOS = {
        "rut": validar_rut,
        "nombres": v_texto("Los nombres", 80, titulo=True),
        "apellidos": v_texto("Los apellidos", 80, titulo=True),
        "telefono": validar_telefono,
        "email": validar_email,
    }

    def _reglas(self, objeto):
        self._exigir_unico(objeto, self._repo.buscar_por_rut(objeto.rut), "el RUT", objeto.rut)

    def buscar_por_rut(self, rut):
        persona = self._repo.buscar_por_rut(validar_rut(rut))
        if persona is None:
            raise ValidacionError(f"No existe {self.NOMBRE} con ese RUT.")
        return persona
