"""Reglas de Usuario: registro, hash de contraseñas con bcrypt y autenticación."""
import bcrypt

from auxiliares.configuracion import BCRYPT_ROUNDS
from auxiliares.excepciones import AutenticacionError, ValidacionError
from auxiliares.mensajes import MSG_CREDENCIALES
from auxiliares.validaciones import v_texto, validar_email, validar_password
from datos.modelos.usuario import Usuario
from negocio.negocio_base import NegocioBase


class NegocioUsuarios(NegocioBase):
    MODELO = Usuario
    NOMBRE = "el usuario"
    CAMPOS = {
        "nombres": v_texto("Los nombres", 80, titulo=True),
        "apellidos": v_texto("Los apellidos", 80, titulo=True),
        "email": validar_email,
    }

    # ---- contraseñas ----
    @staticmethod
    def _hashear(password):
        sal = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
        return bcrypt.hashpw(password.encode("utf-8"), sal).decode("utf-8")

    @staticmethod
    def _coincide(password, password_hash):
        """Comparación segura entre la contraseña ingresada y el hash guardado."""
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

    # ---- reglas ----
    def _reglas(self, objeto):
        self._exigir_unico(objeto, self._repo.buscar_por_email(objeto.email),
                           "el correo", objeto.email)

    def registro_abierto(self):
        """El registro sin sesión solo se permite para crear el primer usuario.
        Con usuarios existentes, las cuentas nuevas se crean desde el módulo Usuarios."""
        return self._repo.contar() == 0

    def registrar_usuario(self, datos, password, confirmacion):
        validar_password(password, confirmacion)
        usuario = self._preparar(datos)
        self._reglas(usuario)
        usuario.password_hash = self._hashear(password)
        return self._repo.guardar(usuario)

    def agregar(self, datos):
        raise ValidacionError("Para crear un usuario se necesita contraseña: usa registrar_usuario().")

    def autenticar(self, email, password):
        """Devuelve el usuario si las credenciales son correctas.
        El mensaje de error es el mismo si falla el correo o la contraseña."""
        usuario = self._repo.buscar_por_email(str(email or "").strip().lower())
        if usuario is None or not usuario.habilitado \
                or not self._coincide(str(password or ""), usuario.password_hash):
            raise AutenticacionError(MSG_CREDENCIALES)
        return usuario

    def cambiar_contrasena(self, id_usuario, actual, nueva, confirmacion):
        usuario = self.obtener(id_usuario)
        if not self._coincide(str(actual or ""), usuario.password_hash):
            raise ValidacionError("La contraseña actual es incorrecta.")
        validar_password(nueva, confirmacion)
        usuario.password_hash = self._hashear(nueva)
        return self._repo.guardar(usuario)

    def buscar_por_email(self, email):
        usuario = self._repo.buscar_por_email(validar_email(email))
        if usuario is None:
            raise ValidacionError("No existe un usuario con ese correo.")
        return usuario

    def deshabilitar_usuario(self, id_usuario, id_usuario_en_sesion):
        if id_usuario == id_usuario_en_sesion:
            raise ValidacionError("No puedes deshabilitar tu propia cuenta mientras la usas.")
        self.eliminar(id_usuario)
