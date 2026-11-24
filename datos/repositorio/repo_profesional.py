from datos.modelos.especialidad import Especialidad
from datos.modelos.profesional import Profesional
from datos.repositorio.repo_base import RepoBase


class RepoProfesional(RepoBase):
    MODELO = Profesional

    def _consulta(self):
        return Profesional.select(Profesional, Especialidad).join(Especialidad)

    def buscar_por_rut(self, rut):
        return self._primero(self._consulta().where(Profesional.rut == rut))
