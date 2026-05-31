import ctypes
import win32gui
import win32con

def esta_en_pantalla_completa():
    try:
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return False
        
        rect = win32gui.GetWindowRect(hwnd)
        ancho_pantalla = ctypes.windll.user32.GetSystemMetrics(0)
        alto_pantalla = ctypes.windll.user32.GetSystemMetrics(1)

        ventana_ancho = rect[2] - rect[0]
        ventana_alto = rect[3] - rect[1]

        return ventana_ancho >= ancho_pantalla and ventana_alto >= alto_pantalla
    except:
        return False