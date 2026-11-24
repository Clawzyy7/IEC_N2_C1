from auxiliares.formato import fecha_hora_a_texto
from presentacion.presentacion_base import PresentacionBase


class PresentacionCita(PresentacionBase):
    TITULO = "Citas"
    COLUMNAS = ["ID", "Paciente", "Profesional", "Estado", "Registrada", "Observaciones"]
    CAMPOS = [("observaciones", "Observaciones (opcional)")]   # al modificar solo se editan estas

    def __init__(self, negocio, negocio_estados):
        super().__init__(negocio)
        self._estados = negocio_estados

    def _fila(self, c):
        return [c.id_cita, c.paciente.nombre_completo, c.profesional.nombre_completo,
                c.estado.nombre, fecha_hora_a_texto(c.fecha_registro), c.observaciones]

    def _agregar(self):
        """Una cita nueva siempre se crea con reservar() (estado Reservada)."""
        id_paciente = self._pedir_entero("Id del paciente")
        id_profesional = self._pedir_entero("Id del profesional")
        observaciones = self._pedir_texto("Observaciones (opcional)")
        cita = self._negocio.reservar(id_paciente, id_profesional, observaciones)
        print(f"✔ Cita reservada con id {cita.get_id()}.")

    def _extras(self):
        return [("Confirmar cita", self._confirmar), ("Marcar como atendida", self._atender),
                ("Cancelar cita", self._cancelar), ("Listar citas con filtros", self._filtrar)]

    def _confirmar(self):
        self._negocio.confirmar(self._pedir_entero("Id de la cita"))
        print("✔ Cita confirmada.")

    def _atender(self):
        self._negocio.atender(self._pedir_entero("Id de la cita"))
        print("✔ Cita marcada como atendida.")

    def _cancelar(self):
        self._negocio.cancelar(self._pedir_entero("Id de la cita"))
        print("✔ Cita cancelada.")

    def _filtrar(self):
        print("Estados disponibles:")
        for e in self._estados.listar():
            print(f"  {e.id_estado}. {e.nombre}")
        id_paciente = self._pedir_entero("Id del paciente", opcional=True)
        id_profesional = self._pedir_entero("Id del profesional", opcional=True)
        id_estado = self._pedir_entero("Id del estado", opcional=True)
        self._mostrar_tabla(self._negocio.listar_citas(id_paciente, id_profesional, id_estado))
