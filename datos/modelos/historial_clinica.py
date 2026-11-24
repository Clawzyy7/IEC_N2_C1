from datetime import datetime

from peewee import AutoField, CharField, DateTimeField, ForeignKeyField

from datos.modelos.cita import Cita
from datos.modelos.ficha_paciente import FichaPaciente
from datos.model_base import ModelBase
from datos.modelos.paciente import Paciente


class HistorialClinica(ModelBase):
    id_historial = AutoField()
    ficha = ForeignKeyField(FichaPaciente, column_name="id_ficha", backref="historiales")
    paciente = ForeignKeyField(Paciente, column_name="id_paciente", backref="historiales")
    cita = ForeignKeyField(Cita, column_name="id_cita", backref="historiales")
    motivo = CharField(max_length=255)
    diagnostico = CharField(max_length=500, default="")
    tratamiento = CharField(max_length=500, default="")
    observaciones = CharField(max_length=255, default="")
    fecha_actualizacion = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "historial_clinica"
