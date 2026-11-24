"""Excepciones propias de la aplicación."""


class ValidacionError(Exception):
    """Un dato no cumple una regla de validación o de negocio."""


class ErrorBaseDatos(Exception):
    """Fallo al conectar o ejecutar algo en la base de datos."""


class AutenticacionError(Exception):
    """Credenciales inválidas en el inicio de sesión."""
