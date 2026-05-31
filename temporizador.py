import threading
from tts import hablar

timers = []

def iniciar_temporizador(minutos, mensaje="El temporizador ha terminado"):
    segundos = minutos * 60

    def _avisar():
        import winsound
        winsound.Beep(1000, 500)
        winsound.Beep(1000, 500)
        winsound.Beep(1000, 500)
        hablar(mensaje)

    t = threading.Timer(segundos, _avisar)
    t.daemon = True
    t.start()
    timers.append(t)
    return f"Temporizador de {minutos} minutos iniciado."

def cancelar_temporizadores():
    for t in timers:
        t.cancel()
    timers.clear()
    return "Temporizadores cancelados."