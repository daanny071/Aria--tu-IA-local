import threading
import re
from datetime import datetime, timedelta
import winsound

recordatorios = []

def iniciar_recordatorio(texto_completo, hablar_func):
    # Extrae la hora si dice "a las X"
    hora_match = re.search(r'a las (\d+)(?::(\d+))?', texto_completo.lower())
    # Extrae minutos si dice "en X minutos"
    minutos_match = re.search(r'en (\d+) minutos', texto_completo.lower())

    # Extrae el mensaje (lo que hay después de "que")
    mensaje_match = re.search(r'\bque\b(.+)', texto_completo.lower())
    mensaje = mensaje_match.group(1).strip() if mensaje_match else "tienes un recordatorio"

    if hora_match:
        hora = int(hora_match.group(1))
        minuto = int(hora_match.group(2)) if hora_match.group(2) else 0
        ahora = datetime.now()
        objetivo = ahora.replace(hour=hora, minute=minuto, second=0)
        if objetivo < ahora:
            objetivo += timedelta(days=1)
        segundos = (objetivo - ahora).total_seconds()
        hora_str = f"las {hora}:{minuto:02d}"
    elif minutos_match:
        minutos = int(minutos_match.group(1))
        segundos = minutos * 60
        hora_str = f"{minutos} minutos"
    else:
        return "No entendí cuándo quieres el recordatorio."

    def _avisar():
        winsound.Beep(1000, 300)
        winsound.Beep(1000, 300)
        hablar_func(f"Recordatorio: {mensaje}")

    t = threading.Timer(segundos, _avisar)
    t.daemon = True
    t.start()
    recordatorios.append(t)
    return f"Recordatorio puesto para {hora_str}: {mensaje}."

def cancelar_recordatorios():
    for t in recordatorios:
        t.cancel()
    recordatorios.clear()
    return "Recordatorios cancelados."