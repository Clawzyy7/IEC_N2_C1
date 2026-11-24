from datos.modelos.paciente import Paciente
from datos.repositorio.repo_base import RepoBase


class RepoPaciente(RepoBase):
    MODELO = Paciente

    def buscar_por_rut(self, rut):
        return self._primero(self._consulta().where(Paciente.rut == rut))
