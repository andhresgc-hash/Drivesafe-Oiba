from datetime import datetime
import re
from vehiculos import registrar_vehiculo
from usuarios import registrar_usuario, iniciar_sesion
from citas import (
    obtener_instructores, 
    obtener_vehiculos, 
    programar_cita, 
    obtener_citas_pendientes_estudiante, 
    obtener_historial_estudiante,
    verificar_disponibilidad,
    obtener_citas_pendientes_instructor,
    confirmar_clase,                      
    obtener_historial_instructor,
    obtener_citas_pendientes_instructor_por_fecha,
    buscar_cedula_instructor_por_nombre,
    obtener_nombre_usuario)

def pedir_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print("\nERROR: Entrada inválida. Por favor digite un número válido, no letras.\n")

def pedir_nombre(mensaje):
    while True:
        nombre = input(mensaje).strip()
        if nombre and nombre.replace(" ", "").isalpha():
            return nombre
        print("\nERROR: Nombre inválido. Debe contener solo letras y espacios, y no estar vacío.\n")

def pedir_edad(mensaje):
    while True:
        edad = pedir_entero(mensaje)
        if 16 <= edad <= 90:
            return edad
        print("\nERROR: Edad inválida. Debe estar entre 16 y 90 años.\n")

def pedir_curso(mensaje):
    while True:
        curso = input(mensaje).strip().lower()
        if curso in ["carro", "moto"]:
            return curso
        print("\nERROR: Entrada inválida. Escriba exactamente 'Carro' o 'Moto'.\n")

def pedir_placa(mensaje):
    while True:
        placa = input(mensaje).strip().upper()
        if re.match(r"^[A-Z]{3}-?[0-9]{3}$", placa):
            return placa
        print("\nERROR: Placa inválida. Debe tener exactamente 3 letras seguidas de 3 números (ejemplo: ABC-123 o ABC123).\n")

def pedir_cedula(mensaje):
    while True:
        cedula = pedir_entero(mensaje)
        if 100000 <= cedula <= 9999999999:
            return cedula
        print("\nERROR: Cédula inválida. Debe tener entre 6 y 10 dígitos.\n")

def pedir_modelo(mensaje):
    while True:
        año = pedir_entero(mensaje)
        if 1900 <= año <= 2030:
            return año
        print("\nERROR: Modelo (año) inválido. Debe ser un año entre 1900 y 2030.\n")

def pedir_fecha(mensaje):
    while True:
        fecha_str = input(mensaje).strip()
        try:
            datetime.strptime(fecha_str, "%d-%m-%Y")
            return fecha_str
        except ValueError:
            print("\nERROR: Fecha inválida. Use el formato DD-MM-AAAA (ejemplo: 20-07-2026).\n")

def pedir_hora(mensaje):
    while True:
        hora_str = input(mensaje).strip()
        try:
            datetime.strptime(hora_str, "%H:%M")
            return hora_str
        except ValueError:
            print("\nERROR: Hora inválida. Use el formato HH:MM en rango 24 horas (ejemplo: 14:00).\n")

def pedir_opcion(mensaje, opciones_validas):
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones_validas:
            return opcion
        print(f"\nERROR: Opción no válida. Por favor, selecciona una de las opciones: {', '.join(opciones_validas)}.\n")

def main():
    while True:
        print("\nBIENVENIDO A DRIVESAFE OIBA")
        print("1. Ingresar como Estudiante")
        print("2. Ingresar como Instructor")
        print("0. Salir de DriveSafe Oiba")
        opcion = pedir_opcion("Elige una opción: ", ["1", "2", "0"])
        if opcion == "1":
            portal_estudiante()
        elif opcion == "2":
            portal_instructor()
        elif opcion == "0":
            print("¡Gracias por usar DriveSafe, bay bay!")
            break

def portal_estudiante():
    while True:
        print("\nPORTAL ESTUDIANTE")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("0. Volver")
        
        opcion = pedir_opcion("Elige una opción: ", ["1", "2", "0"])
        if opcion == "1":
            cedula = input("Cédula: ").strip()
            usuario = iniciar_sesion("estudiantes", cedula)
            if usuario:
                menu_estudiante(usuario)
            else:
                print("Estudiante no encontrado.")
        elif opcion == "2":
            nombre = pedir_nombre("Nombre: ")
            cedula = pedir_cedula("Cédula: ")
            edad = pedir_edad("Edad: ")
            curso = pedir_curso("Curso (Carro/Moto): ")
            exito = registrar_usuario("estudiantes", nombre, cedula, edad, curso)
            if exito:
                print("Estudiante registrado exitosamente!")
            else:
                print("Error: Ya existe alguien con esa cédula.")
                
        elif opcion == "0":
            break

def menu_estudiante(usuario):
    while True:
        print(f"\nHola {usuario['nombre']} (Estudiante)")
        print("1. Clases programadas")
        print("2. Asistencias")
        print("3. Agendar clase")
        print("0. Cerrar sesión")
        opcion = pedir_opcion("Elige una opción: ", ["1", "2", "3", "0"])
        if opcion == "0":
            break
        elif opcion == "1":
            print("\nMis Clases Programadas")
            citas_pendientes = obtener_citas_pendientes_estudiante(usuario['cedula'])
            if len(citas_pendientes) == 0:
                print("No tienes clases programadas por ahora.")
            else:
                for cita in citas_pendientes:
                    nombre_inst = obtener_nombre_usuario("instructores", cita['cedula_instructor'])
                    print(f"ID Cita: {cita['id_cita']}")
                    print(f"Fecha: {cita['fecha']} a las {cita['hora']}")
                    print(f"Duración: {cita.get('duracion', 1)} hora(s)")
                    print(f"Vehículo Placa: {cita['placa_vehiculo']}")
                    print(f"Instructor: {nombre_inst}")
            
        elif opcion == "2":
            print("\nHistorial de Asistencias")
            historial = obtener_historial_estudiante(usuario['cedula'])
            if len(historial) == 0:
                print("Aún no tienes clases asistidas en tu historial.")
            else:
                for cita in historial:
                    nombre_inst = obtener_nombre_usuario("instructores", cita['cedula_instructor'])
                    print(f"Fecha: {cita['fecha']} | Instructor: {nombre_inst}")
                    print(f"Observaciones del Instructor: {cita['observaciones']}")
            
        elif opcion == "3":
            print("\nAgendar Nueva Clase")
            
            tipo_del_estudiante = usuario['detalle']
            print(f"Filtrando disponibilidad para: {tipo_del_estudiante.upper()}")
            
            instructores = obtener_instructores(tipo_del_estudiante)
            if not instructores:
                print(f"No hay instructores de {tipo_del_estudiante} disponibles. Intenta más tarde.")
                continue
                
            print("\nInstructores Disponibles:")
            for cedula, inst in instructores.items():
                print(f"- {inst['nombre']} (Especialidad: {inst['detalle']}) | Cédula: {cedula}")

            vehiculos = obtener_vehiculos(tipo_del_estudiante)
            if not vehiculos:
                print(f"No hay vehículos tipo {tipo_del_estudiante} disponibles. Intenta más tarde.")
                continue
                
            print("\nVehículos Disponibles:")
            for placa, veh in vehiculos.items():
                print(f"- {veh['tipo']} {veh['modelo']} | Placa: {placa}")
            print("\n-- Digite los datos para su clase --")
            fecha = pedir_fecha("Fecha (Día-Mes-Año) (ejemplo 20-07-2026): ") 
            hora = pedir_hora("Hora de inicio (ejemplo 14:00): ")
            duracion = pedir_entero("Duración de la clase (en horas): ") 
            nombre_inst = pedir_nombre("Digite el Nombre del instructor elegido: ")
            id_inst = buscar_cedula_instructor_por_nombre(nombre_inst, tipo_del_estudiante)
            if id_inst is None:
                print(f"\nNo se encontró ningún instructor llamado '{nombre_inst}' de especialidad {tipo_del_estudiante}.")
                continue
                
            placa_veh = pedir_placa("Digite la Placa del vehículo elegido: ")
            print("\nVerificando disponibilidad...")
            disponible = verificar_disponibilidad(fecha, hora, duracion, id_inst, placa_veh)
            if disponible:
                programar_cita(usuario['cedula'], fecha, hora, duracion, id_inst, placa_veh)
                print("\nClase agendada exitosamente")
            else:
                print("\nEl instructor o el vehículo ya tienen una clase asignada que se cuzará con ese horario, por favor intenta con otra fecha u otra hora.")

def portal_instructor():
    while True:
        print("\nPORTAL INSTRUCTOR")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("0. Volver pa atras")
        
        opcion = pedir_opcion("Elige una opción: ", ["1", "2", "0"])
        if opcion == "1":
            cedula = input("Cédula: ").strip()
            usuario = iniciar_sesion("instructores", cedula)
            if usuario:
                menu_instructor(usuario)
            else:
                print("Instructor no encontrado.")
                
        elif opcion == "2":
            nombre = pedir_nombre("Nombre: ")
            cedula = pedir_cedula("Cédula: ")
            edad = pedir_edad("Edad: ") 
            especialidad = pedir_curso("Especialidad (Carro/Moto): ")
            exito = registrar_usuario("instructores", nombre, cedula, edad, especialidad)
            if exito:
                print("Instructor registrado exitosamente")
            else:
                print("Ya existe alguien con esa cédula.")
                
        elif opcion == "0":
            break

def menu_instructor(usuario):
    while True:
        print(f"\nHola {usuario['nombre']} (Instructor)")
        print("1. Mis clases programadas")
        print("2. Historial de clases")
        print("3. Registrar un vehículo")
        print("0. Cerrar sesión")
        
        opcion = pedir_opcion("Elige una opción: ", ["1", "2", "3", "0"])
        
        if opcion == "0":
            break
            
        elif opcion == "1":
            print("\nMis Clases Programadas")
            print("1. Ver todas las clases pendientes")
            print("2. Filtrar clases por fecha")
            print("0. Volver")
            
            subopcion = pedir_opcion("Elige una opción: ", ["1", "2", "0"])
            
            mis_citas = []
            if subopcion == "1":
                mis_citas = obtener_citas_pendientes_instructor(usuario['cedula'])
            elif subopcion == "2":
                fecha_buscar = pedir_fecha("Ingresa la fecha a buscar (Día-Mes-Año): ")
                mis_citas = obtener_citas_pendientes_instructor_por_fecha(usuario['cedula'], fecha_buscar)
            elif subopcion == "0":
                continue
            if len(mis_citas) == 0:
                print("\nNo se encontraron clases programadas.")
            else:
                for cita in mis_citas:
                    print(f"ID Cita: {cita['id_cita']}")
                    print(f"Fecha: {cita['fecha']} a las {cita['hora']}")
                    print(f"Estudiante CC: {cita['cedula_estudiante']} | Vehículo: {cita['placa_vehiculo']}")
                confirmar = input("\n¿Deseas confirmar alguna clase como terminada? (Escribe el id de la cita o presiona enter en blanco para volver): ")
                if confirmar != "":
                    observacion = input("Escribe una observación de la clase: ")
                    exito = confirmar_clase(confirmar, observacion)
                    if exito:
                        print("\nClase confirmada exitosamente!")
                    else:
                        print("\nId de cita no encontrado.")

        elif opcion == "2":
            print("\nMi Historial de Clases Terminadas")
            historial = obtener_historial_instructor(usuario['cedula'])
            if len(historial) == 0:
                print("\nAún no tienes clases en tu historial.")
            else:
                for cita in historial:
                    print(f"Fecha: {cita['fecha']} | Estudiante: {cita['cedula_estudiante']}")
                    print(f"Observación: {cita['observaciones']}")

        elif opcion == "3":
            print("\nRegistro de Nuevo Vehículo")
            placa = pedir_placa("Ingrese la placa (Ejemplo: ABC-123): ")
            tipo = pedir_curso("Tipo de vehículo (Carro/Moto): ")
            modelo = pedir_modelo("Modelo (Año): ")
            exito = registrar_vehiculo(placa, tipo, modelo)
            if exito:
                print("Vehículo registrado exitosamente")
            else:
                print("Ya existe un vehículo con esa placa.")
                    
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()