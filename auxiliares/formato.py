"""Conversión de fechas y horas desde/hacia texto."""
from datetime import date, datetime, time, timedelta

from auxiliares.excepciones import ValidacionError

FORMATO_FECHA = "%d/%m/%Y"
FORMATO_HORA = "%H:%M"
FORMATO_FECHA_HORA = "%d/%m/%Y %H:%M"


def a_fecha(valor):
    """Acepta date/datetime, texto dd/mm/aaaa o aaaa-mm-dd y devuelve un date."""
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    texto = str(valor).strip()
    for formato in (FORMATO_FECHA, "%Y-%m-%d"):
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            pass
    raise ValidacionError("Fecha inválida. Usa el formato dd/mm/aaaa (ej: 25/03/1998).")


def a_hora(valor):
    """Acepta time, timedelta (así devuelve MySQL las columnas TIME) o texto HH:MM."""
    if isinstance(valor, time):
        return valor.replace(second=0, microsecond=0)
    if isinstance(valor, timedelta):
        minutos = int(valor.total_seconds() // 60) % (24 * 60)
        return time(minutos // 60, minutos % 60)
    texto = str(valor).strip()
    for formato in ("%H:%M", "%H:%M:%S"):
        try:
            return datetime.strptime(texto, formato).time().replace(second=0)
        except ValueError:
            pass
    raise ValidacionError("Hora inválida. Usa el formato HH:MM (ej: 09:30).")


def fecha_a_texto(fecha):
    return fecha.strftime(FORMATO_FECHA) if fecha else ""


def hora_a_texto(hora):
    return a_hora(hora).strftime(FORMATO_HORA) if hora not in (None, "") else ""


def fecha_hora_a_texto(valor):
    return valor.strftime(FORMATO_FECHA_HORA) if valor else ""


def a_texto(valor):
    """Texto legible para cualquier valor (se usa al mostrar datos actuales)."""
    if valor is None:
        return ""
    if isinstance(valor, datetime):
        return fecha_hora_a_texto(valor)
    if isinstance(valor, date):
        return fecha_a_texto(valor)
    if isinstance(valor, (time, timedelta)):
        return hora_a_texto(valor)
    if isinstance(valor, bool):
        return "Sí" if valor else "No"
    return str(valor)
