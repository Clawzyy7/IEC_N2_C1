from peewee import AutoField, BooleanField, CharField

from datos.model_base import ModelBase


class Especialidad(ModelBase):
    id_especialidad = AutoField()
    nombre = CharField(max_length=80, unique=True, column_name="especialidad")
    descripcion = CharField(max_length=200, default="")
    habilitado = BooleanField(default=True)

    class Meta:
        table_name = "especialidad"
