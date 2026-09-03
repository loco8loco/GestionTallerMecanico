"""
Funciones auxiliares
"""

from datetime import datetime

def formatear_fecha(fecha):
    """Formatea fecha para mostrar"""
    if fecha:
        return fecha.strftime('%d/%m/%Y')
    return ''

def formatear_moneda(cantidad):
    """Formatea cantidad como moneda"""
    return f'€{cantidad:.2f}'

def generar_numero_factura():
    """Genera número de factura único"""
    ahora = datetime.now()
    return f'F-{ahora.year}-{ahora.month:02d}-{ahora.day:02d}-{ahora.microsecond}'
