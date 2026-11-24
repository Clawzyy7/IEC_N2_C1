from datos.modelos.usuario import Usuario
from datos.repositorio.repo_base import RepoBase


class RepoUsuario(RepoBase):
    MODELO = Usuario

    def buscar_por_email(self, email):
        return self._primero(self._consulta().where(Usuario.email == email))

    def contar(self):
        """Cantidad total de usuarios registrados (habilitados o no)."""
        with self._conexion():
            return Usuario.select().count()
