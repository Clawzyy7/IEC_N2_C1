"""Sesion: guarda quién inició sesión. Sin sesión activa no se accede al menú principal."""


class Sesion:
    def __init__(self):
        self._usuario = None

    @property
    def activa(self):
        return self._usuario is not None

    @property
    def usuario(self):
        return self._usuario

    def iniciar(self, usuario):
        self._usuario = usuario

    def cerrar(self):
        self._usuario = None
