"""
conexion.py
Conexión a MySQL con Peewee. Los parámetros vienen de auxiliares.configuracion (archivo .env).
"""
import os

import pymysql
from peewee import MySQLDatabase, PeeweeException

from auxiliares.configuracion import (DB_HOST, DB_NOMBRE, DB_PASSWORD, DB_PORT, DB_USER)
from auxiliares.excepciones import ErrorBaseDatos
from auxiliares.mensajes import MSG_ERROR_BD

RUTA_SQL = os.path.join(os.path.dirname(__file__), "sql")

db = MySQLDatabase(DB_NOMBRE, host=DB_HOST, port=DB_PORT, user=DB_USER,
                   password=DB_PASSWORD, charset="utf8mb4")


def inicializar_bd():
    """Crea la BD si no existe y ejecuta los scripts de datos/sql en orden.
    Los nombres de los scripts empiezan con fecha y hora, así que el orden alfabético
    es el cronológico (y respeta las claves foráneas)."""
    try:
        cn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER,
                             password=DB_PASSWORD, charset="utf8mb4")
        try:
            with cn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NOMBRE}` "
                               "DEFAULT CHARACTER SET utf8mb4")
            cn.commit()
        finally:
            cn.close()

        with db.connection_context():
            for archivo in sorted(f for f in os.listdir(RUTA_SQL) if f.endswith(".sql")):
                with open(os.path.join(RUTA_SQL, archivo), encoding="utf-8") as f:
                    lineas = [l for l in f.read().splitlines() if not l.strip().startswith("--")]
                for sentencia in "\n".join(lineas).split(";"):
                    if sentencia.strip():
                        db.execute_sql(sentencia)
    except (PeeweeException, pymysql.MySQLError) as error:
        raise ErrorBaseDatos(MSG_ERROR_BD.format(error=error))
