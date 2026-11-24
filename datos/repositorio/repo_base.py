"""RepoBase: operaciones comunes de acceso a datos con Peewee. Cada repositorio hereda de aquí."""
from abc import ABC
from contextlib import contextmanager

from peewee import IntegrityError, PeeweeException

from auxiliares.excepciones import ErrorBaseDatos
from auxiliares.mensajes import MSG_DUPLICADO, MSG_EN_USO, MSG_ERROR_BD, MSG_REFERENCIA
from datos.conexion import db


def _traducir(error):
    """Convierte los errores de integridad de MySQL en mensajes entendibles."""
    codigo = error.args[0] if error.args and isinstance(error.args[0], int) else None
    return {1062: MSG_DUPLICADO, 1451: MSG_EN_USO, 1452: MSG_REFERENCIA}.get(
        codigo, MSG_ERROR_BD.format(error=error))


class RepoBase(ABC):
    MODELO = None            # cada repositorio indica su modelo Peewee
    CON_HABILITADO = True    # False en tablas con borrado real (cita, ficha, historial)

    @contextmanager
    def _conexion(self):
        """Abre la conexión, la cierra al terminar y traduce los errores de la BD."""
        try:
            with db.connection_context():
                yield
        except IntegrityError as error:
            raise ErrorBaseDatos(_traducir(error))
        except PeeweeException as error:
            raise ErrorBaseDatos(MSG_ERROR_BD.format(error=error))

    def _consulta(self):
        """Consulta base. Los repositorios con relaciones la sobrescriben agregando joins."""
        return self.MODELO.select()

    def _pk(self):
        return self.MODELO._meta.primary_key

    def _primero(self, consulta):
        with self._conexion():
            return consulta.first()

    def _todos(self, consulta):
        with self._conexion():
            return list(consulta)

    # ---- CRUD ----
    def guardar(self, objeto):
        """Inserta (objeto nuevo) o actualiza (objeto existente) usando save()."""
        with self._conexion():
            objeto.save()
        return objeto

    def obtener_por_id(self, id_):
        return self._primero(self._consulta().where(self._pk() == id_))

    def listar(self, solo_habilitados=True):
        consulta = self._consulta()
        if self.CON_HABILITADO and solo_habilitados:
            consulta = consulta.where(self.MODELO.habilitado == True)  # noqa: E712
        return self._todos(consulta.order_by(self._pk()))

    def deshabilitar(self, objeto):
        """Baja lógica: habilitado = 0."""
        objeto.habilitado = False
        return self.guardar(objeto)

    def eliminar(self, objeto):
        """Borrado real."""
        with self._conexion():
            objeto.delete_instance()
