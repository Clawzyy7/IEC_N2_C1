from datos.modelos.estado import Estado
from datos.repositorio.repo_base import RepoBase


class RepoEstado(RepoBase):
    MODELO = Estado

    def buscar_por_nombre(self, nombre):
        return self._primero(self._consulta().where(Estado.nombre == nombre))
