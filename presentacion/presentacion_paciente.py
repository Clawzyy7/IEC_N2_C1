from auxiliares.formato import fecha_a_texto, fecha_hora_a_texto
from presentacion.presentacion_base import PresentacionBase
from prettytable import PrettyTable


class PresentacionPaciente(PresentacionBase):
    TITULO = "Pacientes"
    COLUMNAS = ["ID", "RUT", "Nombre", "Nacimiento", "Teléfono", "Correo"]
    CAMPOS = [("rut", "RUT (ej: 12.345.678-5)"), ("nombres", "Nombres"),
              ("apellidos", "Apellidos"), ("fecha_nacimiento", "Fecha de nacimiento (dd/mm/aaaa)"),
              ("telefono", "Teléfono (ej: +56912345678)"), ("email", "Correo")]

    def _fila(self, p):
        return [p.id_paciente, p.rut, p.nombre_completo, fecha_a_texto(p.fecha_nacimiento),
                p.telefono, p.email]

    def _extras(self):
        return [("Buscar por RUT", self._buscar_por_rut),
                ("Solicitar cita", self._solicitar_cita),
                ("Consultar historial", self._consultar_historial)]

    def _buscar_por_rut(self):
        self._mostrar_tabla([self._negocio.buscar_por_rut(self._pedir_texto("RUT"))])

    def _solicitar_cita(self):
        id_paciente = self._pedir_entero("Id del paciente")
        id_profesional = self._pedir_entero("Id del profesional")
        observaciones = self._pedir_texto("Observaciones (opcional)")
        cita = self._negocio.solicitar_cita(id_paciente, id_profesional, observaciones)
        print(f"✔ Cita reservada con id {cita.get_id()}.")

    def _consultar_historial(self):
        historial = self._negocio.consultar_historial(self._pedir_entero("Id del paciente"))
        if not historial:
            print("El paciente no tiene historial.")
            return
        tabla = PrettyTable(["ID", "Cita", "Motivo", "Diagnóstico", "Tratamiento", "Actualizado"])
        tabla.align = "l"
        for h in historial:
            tabla.add_row([h.id_historial, h.__data__.get("cita"), h.motivo, h.diagnostico,
                           h.tratamiento, fecha_hora_a_texto(h.fecha_actualizacion)])
        print(tabla)
