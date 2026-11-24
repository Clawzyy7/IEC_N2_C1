from peewee import AutoField, CharField, ForeignKeyField

from datos.model_base import ModelBase
from datos.modelos.paciente import Paciente


class FichaPaciente(ModelBase):
    id_ficha = AutoField()
    paciente = ForeignKeyField(Paciente, column_name="id_paciente", unique=True,
                               backref="fichas")          # relación 1:1
    motivo = CharField(max_length=255)
    diagnostico = CharField(max_length=500, default="")
    tratamiento = CharField(max_length=500, default="")

    class Meta:
        table_name = "ficha_paciente"
