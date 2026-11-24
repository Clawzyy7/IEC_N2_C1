from peewee import AutoField, BooleanField, CharField, ForeignKeyField

from datos.modelos.especialidad import Especialidad
from datos.model_base import ModelBase
from datos.modelos.persona import PersonaMixin


class Profesional(PersonaMixin, ModelBase):
    id_profesional = AutoField()
    rut = CharField(max_length=12, unique=True)
    nombres = CharField(max_length=80)
    apellidos = CharField(max_length=80)
    especialidad = ForeignKeyField(Especialidad, column_name="id_especialidad",
                                   backref="profesionales")
    telefono = CharField(max_length=15)
    email = CharField(max_length=100)
    habilitado = BooleanField(default=True)

    class Meta:
        table_name = "profesional"
