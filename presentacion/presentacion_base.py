"""PresentacionBase: menú CRUD genérico por consola. Solo habla con la capa de negocio.
Cada hija define sus CAMPOS, COLUMNAS y cómo se muestra una fila (polimorfismo)."""
from abc import ABC, abstractmethod

from prettytable import PrettyTable

from auxiliares.excepciones import ErrorBaseDatos, ValidacionError
from auxiliares.formato import a_texto
from auxiliares.mensajes import (MSG_ENTER_CONSERVA, MSG_ENTERO_INVALIDO, MSG_ELIMINADO,
                                 MSG_ERROR, MSG_ERROR_CAMPO, MSG_GUARDADO, MSG_MODIFICADO,
                                 MSG_OPCION_INVALIDA, MSG_SIN_REGISTROS)


class PresentacionBase(ABC):
    TITULO = ""
    COLUMNAS = []              # encabezados de la tabla
    CAMPOS = []                # [(campo, etiqueta)] que se piden al crear y al modificar
    CAMPOS_SOLO_CREAR = []     # [(campo, etiqueta)] que solo se piden al crear
    ETIQUETA_ELIMINAR = "Eliminar"

    def __init__(self, negocio):
        self._negocio = negocio

    # ---- lo que cada hija define ----
    @abstractmethod
    def _fila(self, objeto):
        """Lista de valores de una fila de la tabla (en el orden de COLUMNAS)."""

    def _extras(self):
        """Lista de (etiqueta, método) con acciones propias del módulo."""
        return []

    # ---- entrada de datos ----
    @staticmethod
    def _pedir_entero(etiqueta, opcional=False):
        while True:
            texto = input(f"{etiqueta}{' (Enter = todos)' if opcional else ''}: ").strip()
            if opcional and not texto:
                return None
            try:
                return int(texto)
            except ValueError:
                print(MSG_ENTERO_INVALIDO)

    @staticmethod
    def _pedir_texto(etiqueta):
        return input(f"{etiqueta}: ").strip()

    def _pedir_campo(self, campo, etiqueta, actual=None):
        """Repite la pregunta hasta que el negocio acepte el valor."""
        while True:
            sufijo = f" [{a_texto(actual)}]" if actual is not None else ""
            texto = input(f"{etiqueta}{sufijo}: ").strip()
            if actual is not None and not texto:
                return ""                       # Enter = dejar el valor actual
            try:
                self._negocio.validar_campo(campo, texto)
                return texto
            except ValidacionError as error:
                print(MSG_ERROR_CAMPO.format(error=error))

    def _pedir_datos(self, existente=None):
        datos = {}
        if existente is None:
            for campo, etiqueta in self.CAMPOS_SOLO_CREAR:
                datos[campo] = self._pedir_campo(campo, etiqueta)
        else:
            print(MSG_ENTER_CONSERVA)
        for campo, etiqueta in self.CAMPOS:
            actual = existente.__data__.get(campo) if existente is not None else None
            datos[campo] = self._pedir_campo(campo, etiqueta, actual)
        return datos

    # ---- salida ----
    def _mostrar_tabla(self, objetos):
        if not objetos:
            print(MSG_SIN_REGISTROS)
            return
        tabla = PrettyTable(self.COLUMNAS)
        tabla.align = "l"
        for objeto in objetos:
            tabla.add_row(self._fila(objeto))
        print(tabla)

    # ---- acciones CRUD ----
    def _agregar(self):
        objeto = self._negocio.agregar(self._pedir_datos())
        print(MSG_GUARDADO.format(id=objeto.get_id()))

    def _listar(self):
        self._mostrar_tabla(self._negocio.listar())

    def _buscar_por_id(self):
        self._mostrar_tabla([self._negocio.obtener(self._pedir_entero("Id a buscar"))])

    def _modificar(self):
        self._listar()
        id_ = self._pedir_entero("Id del registro a modificar")
        existente = self._negocio.obtener(id_)
        self._negocio.modificar(id_, self._pedir_datos(existente))
        print(MSG_MODIFICADO)

    def _eliminar(self):
        self._listar()
        self._negocio.eliminar(self._pedir_entero(f"Id del registro ({self.ETIQUETA_ELIMINAR.lower()})"))
        print(MSG_ELIMINADO)

    # ---- menú ----
    def ejecutar(self):
        opciones = [("Agregar", self._agregar), ("Listar", self._listar),
                    ("Buscar por id", self._buscar_por_id), ("Modificar", self._modificar),
                    (self.ETIQUETA_ELIMINAR, self._eliminar)]
        opciones += self._extras()
        while True:
            print(f"\n--- {self.TITULO} ---")
            for numero, (etiqueta, _) in enumerate(opciones, 1):
                print(f"{numero}. {etiqueta}")
            print("0. Volver")
            eleccion = input("Opción: ").strip()
            if eleccion == "0":
                return
            if not (eleccion.isdigit() and 1 <= int(eleccion) <= len(opciones)):
                print(MSG_OPCION_INVALIDA)
                continue
            try:
                opciones[int(eleccion) - 1][1]()
            except (ValidacionError, ErrorBaseDatos) as error:
                print(MSG_ERROR.format(error=error))
