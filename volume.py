import subprocess
import os

NIRCMD = r"D:\ARIA\nircmd.exe"

def subir_volumen(cantidad=10):
    subprocess.run(f'"{NIRCMD}" changesysvolume 6553', shell=True)
    return "Volumen subido."

def bajar_volumen(cantidad=10):
    subprocess.run(f'"{NIRCMD}" changesysvolume -6553', shell=True)
    return "Volumen bajado."

def silenciar():
    subprocess.run(f'"{NIRCMD}" mutesysvolume 1', shell=True)
    return "Silenciado."

def activar_sonido():
    subprocess.run(f'"{NIRCMD}" mutesysvolume 0', shell=True)
    return "Sonido activado."

def volumen_actual():
    return "No puedo consultar el volumen exacto, pero puedo subirlo o bajarlo."