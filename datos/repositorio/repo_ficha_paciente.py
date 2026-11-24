from datos.modelos.ficha_paciente import FichaPaciente
from datos.modelos.paciente import Paciente
from datos.repositorio.repo_base import RepoBase


class RepoFichaPaciente(RepoBase):
    MODELO = FichaPaciente
    CON_HABILITADO = False      # borrado real

    def _consulta(self):
        return FichaPaciente.select(FichaPaciente, Paciente).join(Paciente)

    def buscar_por_paciente(self, id_paciente):
        return self._primero(self._consulta().where(FichaPaciente.paciente == id_paciente))
