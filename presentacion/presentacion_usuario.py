"""Gestión de usuarios (requiere sesión iniciada). La contraseña se pide oculta con Maskpass."""
import maskpass

from auxiliares.excepciones import ValidacionError
from auxiliares.formato import fecha_hora_a_texto
from auxiliares.mensajes import MSG_ELIMINADO, MSG_GUARDADO
from presentacion.presentacion_base import PresentacionBase


def pedir_contrasena(etiqueta="Contraseña"):
    """Pide una contraseña sin mostrarla en pantalla."""
    return maskpass.askpass(prompt=f"{etiqueta}: ", mask="*")


class PresentacionUsuario(PresentacionBase):
    TITULO = "Usuarios"
    COLUMNAS = ["ID", "Nombre", "Correo", "Creado"]
    CAMPOS = [("nombres", "Nombres"), ("apellidos", "Apellidos"), ("email", "Correo")]
    ETIQUETA_ELIMINAR = "Deshabilitar usuario"

    def __init__(self, negocio, sesion):
        super().__init__(negocio)
        self._sesion = sesion

    def _fila(self, u):
        return [u.id_usuario, u.nombre_completo, u.email, fecha_hora_a_texto(u.fecha_creacion)]

    def _agregar(self):
        usuario = registrar_usuario_interactivo(self, self._negocio)
        print(MSG_GUARDADO.format(id=usuario.get_id()))

    def _eliminar(self):
        self._listar()
        id_ = self._pedir_entero("Id del usuario a deshabilitar")
        self._negocio.deshabilitar_usuario(id_, self._sesion.usuario.get_id())
        print(MSG_ELIMINADO)

    def _extras(self):
        return [("Buscar por correo", self._buscar_por_correo),
                ("Cambiar mi contraseña", self._cambiar_contrasena)]

    def _buscar_por_correo(self):
        self._mostrar_tabla([self._negocio.buscar_por_email(self._pedir_texto("Correo"))])

    def _cambiar_contrasena(self):
        actual = pedir_contrasena("Contraseña actual")
        nueva = pedir_contrasena("Nueva contraseña")
        confirmacion = pedir_contrasena("Repita la nueva contraseña")
        self._negocio.cambiar_contrasena(self._sesion.usuario.get_id(), actual, nueva, confirmacion)
        print("✔ Contraseña actualizada.")


def registrar_usuario_interactivo(presentacion, negocio_usuarios):
    """Pide los datos del usuario (validando campo a campo) y su contraseña oculta."""
    datos = {campo: presentacion._pedir_campo(campo, etiqueta)
             for campo, etiqueta in PresentacionUsuario.CAMPOS}
    password = pedir_contrasena()
    confirmacion = pedir_contrasena("Repita la contraseña")
    return negocio_usuarios.registrar_usuario(datos, password, confirmacion)
