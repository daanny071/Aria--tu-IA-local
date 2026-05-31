import subprocess
import os

def apagar(minutos=0):
    segundos = minutos * 60
    os.system(f"shutdown /s /t {segundos}")
    if minutos == 0:
        return "Apagando el PC ahora."
    return f"El PC se apagará en {minutos} minutos."

def reiniciar(minutos=0):
    segundos = minutos * 60
    os.system(f"shutdown /r /t {segundos}")
    if minutos == 0:
        return "Reiniciando el PC ahora."
    return f"El PC se reiniciará en {minutos} minutos."

def cancelar_apagado():
    os.system("shutdown /a")
    return "Apagado cancelado."

def bloquear():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    return "PC bloqueado."

def captura_pantalla():
    import mss
    from PIL import Image
    import datetime
    ruta = os.path.join(os.path.expanduser("~"), "Desktop", f"captura_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img.save(ruta)
    return f"Captura guardada en el escritorio."

def siguiente_cancion():
    import ctypes
    ctypes.windll.user32.keybd_event(0xB0, 0, 0, 0)
    ctypes.windll.user32.keybd_event(0xB0, 0, 2, 0)
    return "Siguiente canción."

def cancion_anterior():
    import ctypes
    ctypes.windll.user32.keybd_event(0xB1, 0, 0, 0)
    ctypes.windll.user32.keybd_event(0xB1, 0, 2, 0)
    return "Canción anterior."

def pausar_musica():
    import ctypes
    ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
    ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)
    return "Música pausada."