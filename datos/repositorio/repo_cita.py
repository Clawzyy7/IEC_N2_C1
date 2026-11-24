from datos.modelos.cita import Cita
from datos.modelos.estado import Estado
from datos.modelos.paciente import Paciente
from datos.modelos.profesional import Profesional
from datos.repositorio.repo_base import RepoBase


class RepoCita(RepoBase):
    MODELO = Cita
    CON_HABILITADO = False      # borrado real

    def _consulta(self):
        return (Cita.select(Cita, Paciente, Profesional, Estado)
                .join(Paciente).switch(Cita)
                .join(Profesional).switch(Cita)
                .join(Estado))

    def listar_filtrado(self, id_paciente=None, id_profesional=None, id_estado=None):
        consulta = self._consulta()
        if id_paciente is not None:
            consulta = consulta.where(Cita.paciente == id_paciente)
        if id_profesional is not None:
            consulta = consulta.where(Cita.profesional == id_profesional)
        if id_estado is not None:
            consulta = consulta.where(Cita.estado == id_estado)
        return self._todos(consulta.order_by(Cita.id_cita))
