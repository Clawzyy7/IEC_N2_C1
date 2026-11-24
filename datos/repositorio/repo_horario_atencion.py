from datos.modelos.horario_atencion import HorarioAtencion
from datos.modelos.profesional import Profesional
from datos.repositorio.repo_base import RepoBase


class RepoHorarioAtencion(RepoBase):
    MODELO = HorarioAtencion

    def _consulta(self):
        return HorarioAtencion.select(HorarioAtencion, Profesional).join(Profesional)

    def listar_por_profesional(self, id_profesional):
        consulta = (self._consulta()
                    .where((HorarioAtencion.profesional == id_profesional)
                           & (HorarioAtencion.habilitado == True))  # noqa: E712
                    .order_by(HorarioAtencion.fecha, HorarioAtencion.hora_inicio))
        return self._todos(consulta)

    def listar_por_profesional_fecha(self, id_profesional, fecha):
        consulta = (self._consulta()
                    .where((HorarioAtencion.profesional == id_profesional)
                           & (HorarioAtencion.fecha == fecha)
                           & (HorarioAtencion.habilitado == True))  # noqa: E712
                    .order_by(HorarioAtencion.hora_inicio))
        return self._todos(consulta)
