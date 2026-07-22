# DriveSafe - Sistema para Clases de Conducción

Bienvenidos al manual de DriveSafe, una aplicación en consola desarrollada en Python y diseñada para organizar de manera eficiente las clases prácticas de carros y motos en una academia de conducción. El propósito principal del programa es la gestión y asignación de horarios para evitar cruces entre instructores, estudiantes y vehículos.

---

## Estructura del Proyecto

A continuación, se detalla la función de cada archivo que compone el sistema:

*   **`mayn.py`**: Es el archivo principal y el punto de inicio de la aplicación. Se encarga de mostrar y controlar todos los menús interactivos en la pantalla.
*   **`usuarios.py`**: Se encarga del registro e inicio de sesión de los estudiantes y los instructores a través de su número de cédula.
*   **`citas.py`**: Gestiona la programación de las clases prácticas. Revisa la disponibilidad de profesores y vehículos a la hora solicitada, y permite registrar las observaciones de rendimiento.
*   **`vehiculos.py`**: Administra la información básica de los carros y motos de la academia (placa, modelo y tipo).
*   **`persistencia.py`**: Permite guardar y cargar la información del sistema en archivos JSON en la carpeta `data`, evitando que se pierdan los datos guardados al cerrar el programa.

---

## Requisitos del Sistema

*   Tener instalado Python en el equipo.

---

## Instrucciones de Uso

### 1. Iniciar la aplicación

Para iniciar la aplicación, simplemente abra la carpeta del proyecto en su editor de código:

1. Abra el archivo principal llamado `mayn.py`.
2. Presione el botón de ejecutar (el ícono de la flecha en la esquina superior derecha).
3. O abra la terminal integrada de su editor y ejecute:
   ```
   python mayn.py
   ```

### 2. Opciones principales del sistema

La aplicación está dividida según el perfil del usuario:

*   **Perfil Estudiante:**
    *   Registro e inicio de sesión con el número de cédula.
    *   Consulta de clases programadas pendientes.
    *   Historial de clases asistidas con las observaciones hechas por el instructor.
    *   Agendamiento de nuevas clases seleccionando instructor y vehículo disponibles.
*   **Perfil Instructor:**
    *   Registro e inicio de sesión con el número de cédula.
    *   Visualización de clases asignadas y filtro por fecha.
    *   Confirmación de finalización de clases e ingreso de comentarios de desempeño.
    *   Visualización del historial de clases impartidas.
    *   Registro de nuevos vehículos para la academia.

---

## Ejemplo de Flujo Completo

Para probar el correcto funcionamiento del sistema paso a paso, se sugiere el siguiente flujo:

1.  **Registrar un Instructor:** Ingresar al menú de Instructores -> Opción registrarse (ej. Nombre: `Carlos Perez`, Cédula: `123`, Edad: `35`, Especialidad: `Carro`).
2.  **Registrar un Vehículo:** Iniciar sesión con la cédula del instructor creado (`123`) y seleccionar la opción de registro de vehículo (ej. Placa: `ABC-123`, Modelo: `2024`, Tipo: `Carro`).
3.  **Registrar un Estudiante:** Regresar al menú principal, entrar al menú de Estudiantes -> Opción registrarse (ej. Nombre: `Laura Gomez`, Cédula: `456`, Edad: `20`, Curso: `Carro`).
4.  **Agendar una Clase:** Iniciar sesión con la cédula de la estudiante (`456`), seleccionar la opción de agendar clase e ingresar la fecha, hora y duración. El sistema sugerirá automáticamente al instructor y vehículo creados previamente por ser compatibles.
5.  **Finalizar Clase:** Iniciar sesión con la cédula del instructor (`123`), ir a clases programadas, seleccionar la cita por su ID para marcarla como terminada y agregar la observación de desempeño para la estudiante.
