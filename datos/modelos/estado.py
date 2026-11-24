from peewee import AutoField, BooleanField, CharField

from datos.model_base import ModelBase


class Estado(ModelBase):
    id_estado = AutoField()
    nombre = CharField(max_length=80, unique=True, column_name="estado")
    descripcion = CharField(max_length=200, default="")
    habilitado = BooleanField(default=True)

    class Meta:
        table_name = "estado"
