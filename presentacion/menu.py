"""Menú de la aplicación: primero el acceso (login) y, con sesión activa, el menú principal.
No conoce repositorios: solo presentaciones y la acción de inicializar la BD."""
from auxiliares.excepciones import ErrorBaseDatos, ValidacionError
from auxiliares.info_app import NOMBRE_APP, VERSION
from auxiliares.mensajes import (MSG_BD_LISTA, MSG_DESPEDIDA, MSG_ERROR, MSG_OPCION_INVALIDA,
                                 MSG_SESION_CERRADA, MSG_SIN_BD)
from auxiliares.opciones_menu import MENU_ACCESO


class Menu:
    def __init__(self, sesion, login, modulos, inicializar_bd):
        self._sesion = sesion
        self._login = login
        self._modulos = modulos                  # {"1": PresentacionEspecialidad, ...}
        self._inicializar_bd = inicializar_bd

    def ejecutar(self):
        while True:
            if not self._sesion.activa:
                if not self._menu_acceso():
                    print(MSG_DESPEDIDA)
                    return
            else:
                self._menu_principal()

    def _menu_acceso(self):
        """Devuelve False cuando el usuario elige salir."""
        print(f"\n===== {NOMBRE_APP.upper()} v{VERSION} =====")
        registro_abierto = self._registro_abierto()
        for clave, texto in MENU_ACCESO.items():
            if clave == "2" and not registro_abierto:
                continue                      # ya hay usuarios: no se ofrece crear cuenta
            print(f"{clave}. {texto}")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "0":
                return False
            elif opcion == "1":
                self._login.iniciar_sesion()
            elif opcion == "2":
                self._login.crear_cuenta()
            elif opcion == "9":
                self._inicializar_bd()
                print(MSG_BD_LISTA)
            else:
                print(MSG_OPCION_INVALIDA)
        except (ValidacionError, ErrorBaseDatos) as error:
            print(MSG_ERROR.format(error=error))
            if isinstance(error, ErrorBaseDatos):
                print(MSG_SIN_BD)
        return True

    def _registro_abierto(self):
        """Si la BD aún no existe o no responde, no se ofrece crear cuenta."""
        try:
            return self._login.registro_abierto()
        except ErrorBaseDatos:
            return False

    def _menu_principal(self):
        print(f"\n===== {NOMBRE_APP.upper()} =====  Sesión: {self._sesion.usuario.nombre_completo}")
        for clave in sorted(self._modulos):
            print(f"{clave}. {self._modulos[clave].TITULO}")
        print("0. Cerrar sesión")
        opcion = input("Opción: ").strip()
        if opcion == "0":
            self._sesion.cerrar()
            print(MSG_SESION_CERRADA)
        elif opcion in self._modulos:
            self._modulos[opcion].ejecutar()
        else:
            print(MSG_OPCION_INVALIDA)
