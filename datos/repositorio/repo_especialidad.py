from datos.modelos.especialidad import Especialidad
from datos.repositorio.repo_base import RepoBase


class RepoEspecialidad(RepoBase):
    MODELO = Especialidad

    def buscar_por_nombre(self, nombre):
        return self._primero(self._consulta().where(Especialidad.nombre == nombre))
