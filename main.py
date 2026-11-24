"""
main.py
Arma las capas (datos -> negocio -> presentación) y lanza la aplicación.
El usuario debe iniciar sesión antes de acceder al menú principal.
Ejecutar con:  python main.py
"""
from datos.conexion import inicializar_bd
from datos.repositorio import (RepoCita, RepoEspecialidad, RepoEstado, RepoFichaPaciente,
                                RepoHistorialClinica, RepoHorarioAtencion, RepoPaciente,
                                RepoProfesional, RepoUsuario)
from negocio import (NegocioCitas, NegocioEspecialidades, NegocioEstados, NegocioFichas,
                     NegocioHistoriales, NegocioHorarios, NegocioPacientes,
                     NegocioProfesionales, NegocioUsuarios, Sesion)
from presentacion.menu import Menu
from presentacion.presentacion_cita import PresentacionCita
from presentacion.presentacion_especialidad import PresentacionEspecialidad
from presentacion.presentacion_estado import PresentacionEstado
from presentacion.presentacion_ficha import PresentacionFicha
from presentacion.presentacion_historial import PresentacionHistorial
from presentacion.presentacion_horario import PresentacionHorario
from presentacion.presentacion_login import PresentacionLogin
from presentacion.presentacion_paciente import PresentacionPaciente
from presentacion.presentacion_profesional import PresentacionProfesional
from presentacion.presentacion_usuario import PresentacionUsuario


def main():
    # Capa de datos (repositorios)
    especialidad_repo = RepoEspecialidad()
    estado_repo = RepoEstado()
    profesional_repo = RepoProfesional()
    paciente_repo = RepoPaciente()
    horario_repo = RepoHorarioAtencion()
    cita_repo = RepoCita()
    ficha_repo = RepoFichaPaciente()
    historial_repo = RepoHistorialClinica()
    usuario_repo = RepoUsuario()

    # Capa de negocio
    especialidad_negocio = NegocioEspecialidades(especialidad_repo)
    estado_negocio = NegocioEstados(estado_repo)
    cita_negocio = NegocioCitas(cita_repo, paciente_repo, profesional_repo, estado_repo)
    profesional_negocio = NegocioProfesionales(profesional_repo, especialidad_repo,
                                               horario_repo, cita_negocio)
    paciente_negocio = NegocioPacientes(paciente_repo, historial_repo, cita_negocio)
    horario_negocio = NegocioHorarios(horario_repo, profesional_repo)
    ficha_negocio = NegocioFichas(ficha_repo, paciente_repo)
    historial_negocio = NegocioHistoriales(historial_repo, ficha_repo, cita_repo)
    usuario_negocio = NegocioUsuarios(usuario_repo)
    sesion = Sesion()

    # Capa de presentación (las claves coinciden con el menú del profe: 1 a 8, más 9 = usuarios)
    modulos = {
        "1": PresentacionEspecialidad(especialidad_negocio),
        "2": PresentacionProfesional(profesional_negocio, especialidad_negocio),
        "3": PresentacionHorario(horario_negocio),
        "4": PresentacionPaciente(paciente_negocio),
        "5": PresentacionCita(cita_negocio, estado_negocio),
        "6": PresentacionEstado(estado_negocio),
        "7": PresentacionFicha(ficha_negocio),
        "8": PresentacionHistorial(historial_negocio),
        "9": PresentacionUsuario(usuario_negocio, sesion),
    }
    login = PresentacionLogin(usuario_negocio, sesion)
    Menu(sesion, login, modulos, inicializar_bd).ejecutar()


if __name__ == "__main__":
    main()
