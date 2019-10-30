import sys
from django.core.exceptions import ValidationError

def validate_gmail_email(value):
    if  "gmail" in value :
             raise ValidationError("Su correo no duede ser un gmail")
    else:
        return value




def validaRut(rut):
    """
    Esta funcion cumple el trabajo de realizar la logica de negocio,
    ya sea matematica como logica.
    """
    rfiltro = filtraRut(rut)
    rutx = str(rfiltro[0:len(rfiltro)-1])
    digito = str(rfiltro[-1])
    multiplo = 2
    total = 0
    for reverso in reversed(rutx):
        total += int(reverso) * multiplo
        if multiplo == 7:
            multiplo = 2
        else:
            multiplo += 1
        modulus = total % 11
        verificador = 11 - modulus
        if verificador == 10:
            div = "k"
        elif verificador == 11:
            div = "0"
        else:
            if verificador < 10:
                div = verificador
    if str(div) == str(digito):
        retorno = "Valido"
    else:
        raise ValidationError("Rut NO es Valido")
        retorno = "Invalido"
    return retorno

def filtraRut(rut):
    """
    Esta funcion cumple el trabajo de filtrar el RUN.
    Omitiendo asi los puntos (.) y Guiones (-) y cualquier otro caracter
    que no incluya la variable 'caracteres'.
    """
    caracteres = "1234567890k"
    rutx = ""
    for cambio in rut.lower():
        if cambio in caracteres:
            rutx += cambio
    return rutx