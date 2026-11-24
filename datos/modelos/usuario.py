from datetime import datetime

from peewee import AutoField, BooleanField, CharField, DateTimeField

from datos.model_base import ModelBase
from datos.modelos.persona import PersonaMixin


class Usuario(PersonaMixin, ModelBase):
    id_usuario = AutoField()
    nombres = CharField(max_length=80)
    apellidos = CharField(max_length=80)
    email = CharField(max_length=100, unique=True)
    password_hash = CharField(max_length=60)      # hash bcrypt, nunca la contraseña
    habilitado = BooleanField(default=True)
    fecha_creacion = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "usuario"
