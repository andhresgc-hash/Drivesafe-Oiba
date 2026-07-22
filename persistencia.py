import json
import os

def cargar_datos(archivo):
    if not os.path.exists(archivo):
        return {}
    with open(archivo, 'r') as f:
        return json.load(f)
def guardar_datos(archivo, datos):
    carpeta = os.path.dirname(archivo)
    if carpeta and not os.path.exists(carpeta):
        os.makedirs(carpeta, exist_ok=True)
    with open(archivo, 'w') as f:
        json.dump(datos, f, indent=4)