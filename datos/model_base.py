"""model_base.py
ModelBase de Peewee: centraliza la configuración (la base de datos) de todos los modelos."""
from peewee import Model

from datos.conexion import db


class ModelBase(Model):
    class Meta:
        database = db
