from datetime import date, datetime

from auxiliares.formato import a_hora
from peewee import AutoField, BooleanField, DateField, ForeignKeyField, IntegerField, TimeField

from datos.model_base import ModelBase
from datos.modelos.profesional import Profesional


class HorarioAtencion(ModelBase):
    id_horario = AutoField()
    profesional = ForeignKeyField(Profesional, column_name="id_profesional",
                                  backref="horarios")
    fecha = DateField()
    hora_inicio = TimeField()
    hora_fin = TimeField()
    duracion_bloque = IntegerField()
    habilitado = BooleanField(default=True)

    class Meta:
        table_name = "horario_atencion"

    @property
    def minutos_jornada(self):
        inicio = datetime.combine(date.min, a_hora(self.hora_inicio))
        fin = datetime.combine(date.min, a_hora(self.hora_fin))
        return int((fin - inicio).total_seconds() // 60)

    @property
    def cantidad_bloques(self):
        return self.minutos_jornada // self.duracion_bloque
