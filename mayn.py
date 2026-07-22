from vehiculos import registrar_vehiculo
from usuarios import registrar_usuario, iniciar_sesion
from citas import (
    obtener_instructores, 
    obtener_vehiculos, 
    programar_cita, 
    obtener_citas_instructor,
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
def main():
    while True:
        print("\nBIENVENIDO A DRIVESAFE OIBA")
        print("1. Ingresar como Estudiante")
        print("2. Ingresar como Instructor")
        print("0. Salir de DriveSafe Oiba")
        opcion = input("Elige una opción: ")
        if opcion == "1":
            portal_estudiante()
        elif opcion == "2":
            portal_instructor()
        elif opcion == "0":
            print("¡Gracias por usar DriveSafe, bay bay!")
            break
        else:
            print("Opción no válida, por favor, selecciona 1, 2 o 0.")

def portal_estudiante():
    while True:
        print("\nPORTAL ESTUDIANTE")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("0. Volver")
        
        opcion = input("Elige una opción: ")
        if opcion == "1":
            cedula = input("Cédula: ")
            usuario = iniciar_sesion("estudiantes", cedula)
            if usuario:
                menu_estudiante(usuario)
            else:
                print("Estudiante no encontrado.")
        elif opcion == "2":
            nombre = input("Nombre: ")
            cedula = pedir_entero("Cédula: ")
            edad = pedir_entero("Edad: ")
            curso = input("Curso (Carro/Moto): ")
            exito = registrar_usuario("estudiantes", nombre, cedula, edad, curso)
            if exito:
                print("Estudiante registrado exitosamente!")
            else:
                print("Error: Ya existe alguien con esa cédula.")
                
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")

def menu_estudiante(usuario):
    while True:
        print(f"\nHola {usuario['nombre']} (Estudiante)")
        print("1. Clases programadas")
        print("2. Asistencias")
        print("3. Agendar clase")
        print("0. Cerrar sesión")
        opcion = input("Elige una opción: ")
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
            print("\nDigite los datos para su clase")
            fecha = input("Fecha (Dia-Mes-Año) (ejemplo 20-07-2026): ") 
            hora = input("Hora de inicio (ejemplo 14:00): ")
            duracion = pedir_entero("Duración de la clase (en horas): ") 
            nombre_inst = input("Digite el Nombre del instructor elegido: ")
            id_inst = buscar_cedula_instructor_por_nombre(nombre_inst, tipo_del_estudiante)
            if id_inst is None:
                print(f"\nNo se encontró ningún instructor llamado '{nombre_inst}' de especialidad {tipo_del_estudiante}.")
                continue
                
            placa_veh = input("Digite la Placa del vehículo elegido: ").upper()
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
        
        opcion = input("Elige una opción: ")
        if opcion == "1":
            cedula = input("Cédula: ")
            usuario = iniciar_sesion("instructores", cedula)
            if usuario:
                menu_instructor(usuario)
            else:
                print("Instructor no encontrado.")
                
        elif opcion == "2":
            nombre = input("Nombre: ")
            cedula = pedir_entero("Cédula: ")
            edad = pedir_entero("Edad: ") 
            especialidad = input("Especialidad (Carro/Moto): ")
            exito = registrar_usuario("instructores", nombre, cedula, edad, especialidad)
            if exito:
                print("Instructor registrado exitosamente")
            else:
                print("Ya existe alguien con esa cédula.")
                
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")

def menu_instructor(usuario):
    while True:
        print(f"\nHola {usuario['nombre']} (Instructor)")
        print("1. Mis clases programadas")
        print("2. Historial de clases")
        print("3. Registrar un vehículo")
        print("0. Cerrar sesión")
        
        opcion = input("Elige una opción: ")
        
        if opcion == "0":
            break
            
        elif opcion == "1":
            print("\nMis Clases Programadas")
            print("1. Ver todas las clases pendientes")
            print("2. Filtrar clases por fecha")
            print("0. Volver")
            
            subopcion = input("Elige una opción: ")
            
            mis_citas = []
            if subopcion == "1":
                mis_citas = obtener_citas_pendientes_instructor(usuario['cedula'])
            elif subopcion == "2":
                fecha_buscar = input("Ingresa la fecha a buscar (Dia-Mes-Año): ")
                mis_citas = obtener_citas_pendientes_instructor_por_fecha(usuario['cedula'], fecha_buscar)
            elif subopcion == "0":
                continue
            else:
                print("Opción no válida.")
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
            placa = input("Ingrese la placa (Ejemplo: ABC-123): ")
            tipo = input("Tipo de vehículo (Carro/Moto): ")
            modelo = input("Modelo (Año): ")
            exito = registrar_vehiculo(placa, tipo, modelo)
            if exito:
                print("Vehículo registrado exitosamente")
            else:
                print("Ya existe un vehículo con esa placa.")
                    
        else:
            print("Opción no válida.")
main()