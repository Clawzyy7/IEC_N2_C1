from datetime import datetime

from peewee import AutoField, CharField, DateTimeField, ForeignKeyField

from datos.modelos.estado import Estado
from datos.model_base import ModelBase
from datos.modelos.paciente import Paciente
from datos.modelos.profesional import Profesional


class Cita(ModelBase):
    id_cita = AutoField()
    paciente = ForeignKeyField(Paciente, column_name="id_paciente", backref="citas")
    profesional = ForeignKeyField(Profesional, column_name="id_profesional", backref="citas")
    estado = ForeignKeyField(Estado, column_name="id_estado", backref="citas")
    observaciones = CharField(max_length=255, default="")
    fecha_registro = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "cita"
