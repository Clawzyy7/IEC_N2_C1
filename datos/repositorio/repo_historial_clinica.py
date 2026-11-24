from datos.modelos.historial_clinica import HistorialClinica
from datos.repositorio.repo_base import RepoBase


class RepoHistorialClinica(RepoBase):
    MODELO = HistorialClinica
    CON_HABILITADO = False      # borrado real

    def listar_por_paciente(self, id_paciente):
        consulta = (self._consulta().where(HistorialClinica.paciente == id_paciente)
                    .order_by(HistorialClinica.id_historial))
        return self._todos(consulta)
