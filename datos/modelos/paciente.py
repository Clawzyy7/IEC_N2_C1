from peewee import AutoField, BooleanField, CharField, DateField

from datos.model_base import ModelBase
from datos.modelos.persona import PersonaMixin


class Paciente(PersonaMixin, ModelBase):
    id_paciente = AutoField()
    rut = CharField(max_length=12, unique=True)
    nombres = CharField(max_length=80)
    apellidos = CharField(max_length=80)
    fecha_nacimiento = DateField()
    telefono = CharField(max_length=15)
    email = CharField(max_length=100)
    habilitado = BooleanField(default=True)

    class Meta:
        table_name = "paciente"
