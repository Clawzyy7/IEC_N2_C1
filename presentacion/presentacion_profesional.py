from auxiliares.formato import fecha_a_texto, hora_a_texto
from presentacion.presentacion_base import PresentacionBase
from prettytable import PrettyTable


class PresentacionProfesional(PresentacionBase):
    TITULO = "Profesionales"
    COLUMNAS = ["ID", "RUT", "Nombre", "Especialidad", "Teléfono", "Correo"]
    CAMPOS = [("rut", "RUT (ej: 12.345.678-5)"), ("nombres", "Nombres"),
              ("apellidos", "Apellidos"), ("especialidad", "Id de la especialidad"),
              ("telefono", "Teléfono (ej: +56912345678)"), ("email", "Correo")]

    def __init__(self, negocio, negocio_especialidades):
        super().__init__(negocio)
        self._especialidades = negocio_especialidades

    def _fila(self, p):
        return [p.id_profesional, p.rut, p.nombre_completo, p.especialidad.nombre,
                p.telefono, p.email]

    def _pedir_datos(self, existente=None):
        print("Especialidades disponibles:")
        for e in self._especialidades.listar():
            print(f"  {e.id_especialidad}. {e.nombre}")
        return super()._pedir_datos(existente)

    def _extras(self):
        return [("Buscar por RUT", self._buscar_por_rut),
                ("Consultar agenda", self._consultar_agenda),
                ("Agendar hora", self._agendar_hora)]

    def _buscar_por_rut(self):
        self._mostrar_tabla([self._negocio.buscar_por_rut(self._pedir_texto("RUT"))])

    def _consultar_agenda(self):
        agenda = self._negocio.consultar_agenda(self._pedir_entero("Id del profesional"))
        print(f"\nAgenda de {agenda['profesional'].nombre_completo}")
        print("Jornadas:")
        if agenda["jornadas"]:
            tabla = PrettyTable(["ID", "Fecha", "Inicio", "Fin", "Bloque (min)"])
            tabla.align = "l"
            for j in agenda["jornadas"]:
                tabla.add_row([j.id_horario, fecha_a_texto(j.fecha), hora_a_texto(j.hora_inicio),
                               hora_a_texto(j.hora_fin), j.duracion_bloque])
            print(tabla)
        else:
            print("  (sin jornadas)")
        print("Citas:")
        if agenda["citas"]:
            tabla = PrettyTable(["ID", "Paciente", "Estado", "Observaciones"])
            tabla.align = "l"
            for c in agenda["citas"]:
                tabla.add_row([c.id_cita, c.paciente.nombre_completo, c.estado.nombre,
                               c.observaciones])
            print(tabla)
        else:
            print("  (sin citas)")

    def _agendar_hora(self):
        id_profesional = self._pedir_entero("Id del profesional")
        id_paciente = self._pedir_entero("Id del paciente")
        observaciones = self._pedir_texto("Observaciones (opcional)")
        cita = self._negocio.agendar_hora(id_profesional, id_paciente, observaciones)
        print(f"✔ Hora agendada. Cita id {cita.get_id()}.")
