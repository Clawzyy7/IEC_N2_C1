"""PersonaMixin: comportamiento común de Paciente y Profesional (herencia)."""


class PersonaMixin:
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"
