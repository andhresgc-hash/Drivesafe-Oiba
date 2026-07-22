from persistencia import cargar_datos, guardar_datos
ARCHIVO_USUARIOS = 'data/usuarios.json'
def registrar_usuario(rol, nombre, cedula, edad, especialidad_o_curso):
    datos = cargar_datos(ARCHIVO_USUARIOS)
    if rol not in datos:
        datos[rol] = {}
    if cedula in datos[rol]:
        return False 
    datos[rol][cedula] = {
        'nombre': nombre,
        'cedula': cedula,
        'edad': edad,
        'detalle': especialidad_o_curso
    }
    guardar_datos(ARCHIVO_USUARIOS, datos)
    return True 
def iniciar_sesion(rol, cedula):

    datos = cargar_datos(ARCHIVO_USUARIOS)
    if rol in datos and cedula in datos[rol]:
        return datos[rol][cedula] 
    return None