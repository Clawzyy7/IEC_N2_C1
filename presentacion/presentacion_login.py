"""Inicio de sesión y creación de cuenta. Solo habla con la capa de negocio."""
from auxiliares.configuracion import MAX_INTENTOS_LOGIN
from auxiliares.excepciones import AutenticacionError, ValidacionError
from auxiliares.mensajes import (MSG_BIENVENIDA, MSG_BLOQUEO, MSG_GUARDADO, MSG_INTENTOS,
                                 MSG_REGISTRO_CERRADO)
from presentacion.presentacion_usuario import (PresentacionUsuario, pedir_contrasena,
                                               registrar_usuario_interactivo)


class PresentacionLogin:
    def __init__(self, negocio_usuarios, sesion):
        self._negocio = negocio_usuarios
        self._sesion = sesion
        # reutiliza la pregunta campo a campo de PresentacionUsuario
        self._ayuda_campos = PresentacionUsuario(negocio_usuarios, sesion)

    def iniciar_sesion(self):
        for intento in range(1, MAX_INTENTOS_LOGIN + 1):
            email = input("Correo: ").strip()
            password = pedir_contrasena()
            try:
                usuario = self._negocio.autenticar(email, password)
            except AutenticacionError as error:
                print(f"⚠ {error}")
                restantes = MAX_INTENTOS_LOGIN - intento
                if restantes:
                    print(MSG_INTENTOS.format(n=restantes))
                continue
            self._sesion.iniciar(usuario)
            print(MSG_BIENVENIDA.format(nombre=usuario.nombre_completo))
            return True
        print(MSG_BLOQUEO)
        return False

    def registro_abierto(self):
        return self._negocio.registro_abierto()

    def crear_cuenta(self):
        if not self._negocio.registro_abierto():
            raise ValidacionError(MSG_REGISTRO_CERRADO)
        usuario = registrar_usuario_interactivo(self._ayuda_campos, self._negocio)
        print(MSG_GUARDADO.format(id=usuario.get_id()))
