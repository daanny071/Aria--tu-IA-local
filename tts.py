import edge_tts
import asyncio
import tempfile
import os
from playsound import playsound
import threading
from notificacion import mostrar_notificacion
from perfil import cargar_perfil
from idioma import detectar_idioma, voz_para_idioma

async def _hablar_async(texto, voz):
    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False, dir=tempfile.gettempdir())
    tmp_name = tmp.name
    tmp.close()
    communicate = edge_tts.Communicate(texto, voz, rate="+30%")
    await communicate.save(tmp_name)
    return tmp_name

def hablar(texto, stop_event=None):
    if not texto:
        return

    perfil = cargar_perfil()
    idioma_detectado = detectar_idioma(texto)
    idioma_preferido = perfil.get("idioma_preferido", "es")

    # Si el idioma detectado coincide con el preferido, usa la voz configurada del perfil
    if idioma_detectado == idioma_preferido:
        voz = perfil.get("voz", "es-ES-ElviraNeural")
    else:
        voz = voz_para_idioma(idioma_detectado)

    tmp_name = asyncio.run(_hablar_async(texto, voz))

    if stop_event and stop_event.is_set():
        try:
            os.unlink(tmp_name)
        except:
            pass
        return

    mostrar_notificacion(texto, duracion=8)

    hilo = threading.Thread(target=playsound, args=(tmp_name,), daemon=True)
    hilo.start()

    while hilo.is_alive():
        if stop_event and stop_event.is_set():
            print("⛔ Audio interrumpido.")
            break
        hilo.join(timeout=0.2)

    try:
        os.unlink(tmp_name)
    except:
        pass