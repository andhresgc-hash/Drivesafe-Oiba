from persistencia import cargar_datos, guardar_datos
import uuid 

ARCHIVO_CITAS = 'data/citas.json'
ARCHIVO_USUARIOS = 'data/usuarios.json'
ARCHIVO_VEHICULOS = 'data/vehiculos.json'
from datetime import datetime, timedelta

def verificar_disponibilidad(fecha, hora_inicio, duracion_horas, cedula_instructor, placa_vehiculo):
    citas = cargar_datos(ARCHIVO_CITAS)

    formato = "%d-%m-%Y %H:%M"
    try:
        inicio_nuevo = datetime.strptime(f"{fecha} {hora_inicio}", formato)
        fin_nuevo = inicio_nuevo + timedelta(hours=duracion_horas)
    except ValueError:
        print(">> Error: Formato de fecha u hora incorrecto.")
        return False

    for id_cita, cita in citas.items():
        if cita['asistencia'] != "Completada":
            if str(cita['cedula_instructor']) == str(cedula_instructor) or cita['placa_vehiculo'].lower() == placa_vehiculo.lower():
                inicio_guardado = datetime.strptime(f"{cita['fecha']} {cita['hora']}", formato)
                horas = cita.get('duracion', 1) 
                fin_guardado = inicio_guardado + timedelta(hours=horas)
                
                if inicio_nuevo < fin_guardado and fin_nuevo > inicio_guardado:
                    return False
                    
    return True

def obtener_instructores(tipo_curso):
    datos = cargar_datos(ARCHIVO_USUARIOS)
    instructores_filtrados = {}
    
    if 'instructores' in datos:
        for cedula, inst in datos['instructores'].items():
            if inst['detalle'].lower() == tipo_curso.lower():
                instructores_filtrados[cedula] = inst
                
    return instructores_filtrados

def obtener_vehiculos(tipo_curso):
    datos = cargar_datos(ARCHIVO_VEHICULOS)
    vehiculos_filtrados = {}
    
    for placa, veh in datos.items():
        if veh['tipo'].lower() == tipo_curso.lower():
            vehiculos_filtrados[placa] = veh
            
    return vehiculos_filtrados

def programar_cita(cedula_estudiante, fecha, hora, duracion_horas, cedula_instructor, placa_vehiculo):
    citas = cargar_datos(ARCHIVO_CITAS)
    id_cita = str(uuid.uuid4())[:6] 
    
    citas[id_cita] = {
        'id_cita': id_cita,
        'cedula_estudiante': cedula_estudiante,
        'fecha': fecha,
        'hora': hora,
        'duracion': duracion_horas,
        'cedula_instructor': cedula_instructor,
        'placa_vehiculo': placa_vehiculo,
        'asistencia': None,
        'observaciones': ""
    }
    guardar_datos(ARCHIVO_CITAS, citas)
    return id_cita

def confirmar_clase(id_cita, observacion=""):
    citas = cargar_datos(ARCHIVO_CITAS)
    
    if id_cita in citas:
        citas[id_cita]['asistencia'] = "Completada"
        citas[id_cita]['observaciones'] = observacion
        guardar_datos(ARCHIVO_CITAS, citas)
        return True
    return False

def obtener_citas_pendientes_instructor(cedula_instructor):
    todas = cargar_datos(ARCHIVO_CITAS)
    pendientes = []
    for id_cita, datos in todas.items():
        if datos['cedula_instructor'] == cedula_instructor and datos['asistencia'] == None:
            pendientes.append(datos)
    return pendientes

def obtener_historial_instructor(cedula_instructor):
    todas = cargar_datos(ARCHIVO_CITAS)
    historial = []
    for id_cita, datos in todas.items():
        if datos['cedula_instructor'] == cedula_instructor and datos['asistencia'] == "Completada":
            historial.append(datos)
    return historial

def obtener_citas_pendientes_estudiante(cedula_estudiante):
    todas = cargar_datos(ARCHIVO_CITAS)
    pendientes = []
    for id_cita, datos in todas.items():
        if datos['cedula_estudiante'] == cedula_estudiante and datos['asistencia'] == None:
            pendientes.append(datos)
    return pendientes

def obtener_historial_estudiante(cedula_estudiante):
    todas = cargar_datos(ARCHIVO_CITAS)
    historial = []
    for id_cita, datos in todas.items():
        if datos['cedula_estudiante'] == cedula_estudiante and datos['asistencia'] == "Completada":
            historial.append(datos)
    return historial

def buscar_cedula_instructor_por_nombre(nombre_buscar, tipo_curso):
    datos = cargar_datos(ARCHIVO_USUARIOS)
    if 'instructores' in datos:
        for cedula, inst in datos['instructores'].items():
            if (inst['nombre'].lower() == nombre_buscar.lower() and 
                inst['detalle'].lower() == tipo_curso.lower()):
                return cedula
    return None

def obtener_nombre_usuario(rol, cedula):
    datos = cargar_datos(ARCHIVO_USUARIOS)
    if rol in datos and cedula in datos[rol]:
        return datos[rol][cedula]['nombre']
    return "Desconocido"

def obtener_citas_pendientes_instructor_por_fecha(cedula_instructor, fecha):
    todas = cargar_datos(ARCHIVO_CITAS)
    filtradas = []
    
    for id_cita, datos in todas.items():
        if (datos['cedula_instructor'] == cedula_instructor and 
            datos['asistencia'] == None and 
            datos['fecha'] == fecha):
            filtradas.append(datos)
            
    return filtradas