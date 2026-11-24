from auxiliares.excepciones import ValidacionError
from auxiliares.validaciones import v_entero, v_texto
from datos.modelos.cita import Cita
from negocio.negocio_base import NegocioBase

RESERVADA, CONFIRMADA, ATENDIDA, CANCELADA = "Reservada", "Confirmada", "Atendida", "Cancelada"


class NegocioCitas(NegocioBase):
    MODELO = Cita
    NOMBRE = "la cita"
    CAMPOS = {
        "paciente": v_entero("El id del paciente"),
        "profesional": v_entero("El id del profesional"),
        "observaciones": v_texto("Las observaciones", 255, obligatorio=False),
    }

    def __init__(self, repo_cita, repo_paciente, repo_profesional, repo_estado):
        super().__init__(repo_cita)
        self._pacientes = repo_paciente
        self._profesionales = repo_profesional
        self._estados = repo_estado

    def _reglas(self, objeto):
        self._exigir_activo(self._pacientes, self._id_de(objeto, "paciente"), "el paciente")
        self._exigir_activo(self._profesionales, self._id_de(objeto, "profesional"),
                            "el profesional")
        if self._estados.obtener_por_id(self._id_de(objeto, "estado")) is None:
            raise ValidacionError("La cita no tiene un estado válido.")

    def _estado_por_nombre(self, nombre):
        estado = self._estados.buscar_por_nombre(nombre)
        if estado is None:
            raise ValidacionError(f"Falta el estado '{nombre}'. Inicializa la base de datos.")
        return estado

    # Polimorfismo: sobrecarga (observaciones es opcional)
    def reservar(self, id_paciente, id_profesional, observaciones=""):
        cita = Cita(paciente=self.CAMPOS["paciente"](id_paciente),
                    profesional=self.CAMPOS["profesional"](id_profesional),
                    estado=self._estado_por_nombre(RESERVADA).get_id(),
                    observaciones=self.CAMPOS["observaciones"](observaciones))
        self._reglas(cita)
        return self._repo.guardar(cita)

    # Polimorfismo: sobrescritura (una cita nueva siempre se crea con estado Reservada)
    def agregar(self, datos):
        return self.reservar(datos.get("paciente", ""), datos.get("profesional", ""),
                             datos.get("observaciones", ""))

    def _cambiar_estado(self, id_cita, nuevo, permitidos):
        cita = self.obtener(id_cita)
        actual = cita.estado.nombre
        if actual not in permitidos:
            raise ValidacionError(f"No se puede pasar una cita '{actual}' a '{nuevo}'.")
        cita.estado = self._estado_por_nombre(nuevo).get_id()
        return self._repo.guardar(cita)

    def confirmar(self, id_cita):
        """Reservada -> Confirmada"""
        return self._cambiar_estado(id_cita, CONFIRMADA, (RESERVADA,))

    def atender(self, id_cita):
        """Confirmada -> Atendida"""
        return self._cambiar_estado(id_cita, ATENDIDA, (CONFIRMADA,))

    def cancelar(self, id_cita):
        """Reservada / Confirmada -> Cancelada"""
        return self._cambiar_estado(id_cita, CANCELADA, (RESERVADA, CONFIRMADA))

    # Polimorfismo: sobrecarga (sin argumentos lista todo; con argumentos filtra)
    def listar_citas(self, id_paciente=None, id_profesional=None, id_estado=None):
        return self._repo.listar_filtrado(id_paciente, id_profesional, id_estado)

    def listar(self):
        return self._repo.listar_filtrado()
