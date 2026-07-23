from persistencia import cargar_datos, guardar_datos
ARCHIVO_USUARIOS = 'data/usuarios.json'
def registrar_usuario(rol, nombre, cedula, edad, especialidad_o_curso):
    datos = cargar_datos(ARCHIVO_USUARIOS)
    if rol not in datos:
        datos[rol] = {}
    cedula_str = str(cedula).strip()
    if cedula_str in datos[rol]:
        return False 
    datos[rol][cedula_str] = {
        'nombre': nombre,
        'cedula': int(cedula_str) if cedula_str.isdigit() else cedula_str,
        'edad': edad,
        'detalle': especialidad_o_curso
    }
    guardar_datos(ARCHIVO_USUARIOS, datos)
    return True 

def iniciar_sesion(rol, cedula):
    datos = cargar_datos(ARCHIVO_USUARIOS)
    cedula_str = str(cedula).strip()
    if rol in datos and cedula_str in datos[rol]:
        return datos[rol][cedula_str] 
    return None