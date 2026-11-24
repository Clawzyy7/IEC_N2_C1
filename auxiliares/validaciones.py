"""Validaciones reutilizables. Las funciones v_* fabrican validadores para los CAMPOS de negocio."""
import re
from datetime import date

from auxiliares.excepciones import ValidacionError
from auxiliares.formato import a_fecha, a_hora


def validar_texto(valor, campo, maximo=80, obligatorio=True):
    texto = " ".join(str(valor or "").split())
    if not texto:
        if obligatorio:
            raise ValidacionError(f"{campo} es obligatorio.")
        return ""
    if len(texto) > maximo:
        raise ValidacionError(f"{campo} no puede superar los {maximo} caracteres.")
    return texto


def validar_entero(valor, campo, minimo=1, maximo=None):
    try:
        numero = int(str(valor).strip())
    except ValueError:
        raise ValidacionError(f"{campo} debe ser un número entero.")
    if numero < minimo:
        raise ValidacionError(f"{campo} debe ser mayor o igual a {minimo}.")
    if maximo is not None and numero > maximo:
        raise ValidacionError(f"{campo} debe ser menor o igual a {maximo}.")
    return numero


def _calcular_dv(cuerpo):
    suma, factor = 0, 2
    for digito in reversed(cuerpo):
        suma += int(digito) * factor
        factor = 2 if factor == 7 else factor + 1
    resto = 11 - suma % 11
    return "0" if resto == 11 else "K" if resto == 10 else str(resto)


def validar_rut(rut):
    """Valida con módulo 11 y devuelve el RUT normalizado: 12345678-5."""
    limpio = re.sub(r"[.\s-]", "", str(rut or "")).upper()
    if not re.fullmatch(r"\d{7,8}[\dK]", limpio):
        raise ValidacionError("RUT con formato inválido (ej: 12.345.678-5).")
    cuerpo, dv = limpio[:-1], limpio[-1]
    if _calcular_dv(cuerpo) != dv:
        raise ValidacionError("RUT inválido: el dígito verificador no coincide.")
    return f"{cuerpo}-{dv}"


def validar_email(email):
    email = str(email or "").strip().lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValidacionError("Correo con formato inválido (ej: nombre@correo.cl).")
    if len(email) > 100:
        raise ValidacionError("El correo no puede superar los 100 caracteres.")
    return email


def validar_telefono(telefono):
    limpio = re.sub(r"[\s-]", "", str(telefono or ""))
    if not re.fullmatch(r"\+?\d{8,12}", limpio):
        raise ValidacionError("Teléfono inválido (ej: +56912345678 o 912345678).")
    return limpio


def validar_password(password, confirmacion=None):
    """Mínimo 8 caracteres, con letra y número. bcrypt usa solo los primeros 72 bytes."""
    password = str(password or "")
    if len(password) < 8:
        raise ValidacionError("La contraseña debe tener al menos 8 caracteres.")
    if len(password.encode("utf-8")) > 72:
        raise ValidacionError("La contraseña no puede superar los 72 bytes.")
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        raise ValidacionError("La contraseña debe incluir al menos una letra y un número.")
    if confirmacion is not None and password != confirmacion:
        raise ValidacionError("Las contraseñas no coinciden.")
    return password


def validar_fecha_nacimiento(valor):
    fecha = a_fecha(valor)
    if fecha > date.today():
        raise ValidacionError("La fecha de nacimiento no puede ser futura.")
    return fecha


# ---------- fábricas de validadores (una función de un solo argumento por campo) ----------
def v_texto(campo, maximo=80, obligatorio=True, titulo=False):
    def validador(valor):
        texto = validar_texto(valor, campo, maximo, obligatorio)
        return texto.title() if titulo else texto
    return validador


def v_entero(campo, minimo=1, maximo=None):
    return lambda valor: validar_entero(valor, campo, minimo, maximo)


def v_fecha(campo="La fecha"):
    return lambda valor: a_fecha(valor)


def v_hora(campo="La hora"):
    return lambda valor: a_hora(valor)
