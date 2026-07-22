from persistencia import cargar_datos, guardar_datos
ARCHIVO_VEHICULOS = 'data/vehiculos.json'
def registrar_vehiculo(placa, tipo, modelo):
    datos = cargar_datos(ARCHIVO_VEHICULOS)
    placa = placa.upper()
    if placa in datos:
        return False
    datos[placa] = {
        'placa': placa,
        'tipo': tipo,
        'modelo': modelo,
        'disponible': True
    }
    guardar_datos(ARCHIVO_VEHICULOS, datos)
    return True