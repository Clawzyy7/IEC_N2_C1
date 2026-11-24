"""NegocioBase: reglas comunes de todas las entidades.
Recibe datos como texto desde la presentación, los valida con auxiliares, arma el objeto
del modelo y lo entrega al repositorio. La presentación nunca toca el repositorio."""
from abc import ABC

from auxiliares.excepciones import ValidacionError


class NegocioBase(ABC):
    MODELO = None            # clase Peewee que maneja este negocio
    NOMBRE = "el registro"   # para mensajes de error
    CAMPOS = {}              # campo -> función validadora/convertidora

    def __init__(self, repo):
        self._repo = repo

    # ---- validación y armado del objeto ----
    def validar_campo(self, campo, texto):
        """Valida un campo suelto (la presentación lo usa para repetir la pregunta)."""
        if campo not in self.CAMPOS:
            raise ValidacionError(f"Campo desconocido: {campo}.")
        return self.CAMPOS[campo](str(texto).strip())

    def _preparar(self, datos, existente=None):
        """Crea el objeto (o actualiza el existente). Al modificar, un texto vacío
        deja el valor actual."""
        objeto = existente if existente is not None else self.MODELO()
        for campo, validador in self.CAMPOS.items():
            if existente is not None and not str(datos.get(campo, "")).strip():
                continue
            setattr(objeto, campo, validador(str(datos.get(campo, "")).strip()))
        return objeto

    def _reglas(self, objeto):
        """Reglas de negocio propias; cada hija las sobrescribe (polimorfismo)."""

    # ---- ayudas ----
    @staticmethod
    def _id_de(objeto, campo):
        """Id crudo de una clave foránea (sin cargar el objeto relacionado)."""
        return objeto.__data__.get(campo)

    @staticmethod
    def _exigir_activo(repo, id_, nombre):
        registro = repo.obtener_por_id(id_)
        if registro is None:
            raise ValidacionError(f"No existe {nombre} con id {id_}.")
        if not getattr(registro, "habilitado", True):
            raise ValidacionError(f"{nombre.capitalize()} con id {id_} está deshabilitado/a.")
        return registro

    def _exigir_unico(self, objeto, existente, etiqueta, valor):
        if existente is not None and existente.get_id() != objeto.get_id():
            raise ValidacionError(f"Ya existe {self.NOMBRE} con {etiqueta} {valor}.")

    # ---- CRUD ----
    def agregar(self, datos):
        objeto = self._preparar(datos)
        self._reglas(objeto)
        return self._repo.guardar(objeto)

    def obtener(self, id_):
        registro = self._repo.obtener_por_id(id_)
        if registro is None:
            raise ValidacionError(f"No existe {self.NOMBRE} con id {id_}.")
        return registro

    def modificar(self, id_, datos):
        objeto = self._preparar(datos, self.obtener(id_))
        self._reglas(objeto)
        return self._repo.guardar(objeto)

    def eliminar(self, id_):
        """Baja lógica si la tabla tiene habilitado; borrado real en el resto."""
        objeto = self.obtener(id_)
        if self._repo.CON_HABILITADO:
            self._repo.deshabilitar(objeto)
        else:
            self._repo.eliminar(objeto)

    def listar(self):
        return self._repo.listar()
