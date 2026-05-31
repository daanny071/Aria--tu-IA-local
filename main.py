import keyboard
import threading
import pystray
import winsound
import os
import subprocess
import re
import time
import requests as req
from PIL import Image, ImageDraw
import sys
from capture import capturar_pantalla, capturar_camara
from audio import grabar_hasta_silencio, transcribir
from ai import preguntar
from tts import hablar
from search import buscar
from volume import subir_volumen, bajar_volumen, silenciar, activar_sonido, volumen_actual
from nodisturb import esta_en_pantalla_completa
from sistema import apagar, reiniciar, cancelar_apagado, bloquear, captura_pantalla, siguiente_cancion, cancion_anterior, pausar_musica
from temporizador import iniciar_temporizador, cancelar_temporizadores
from notas import anotar, leer_notas
from utilidades import buscar_youtube, leer_portapapeles
from input_texto import pedir_texto
from calculadora import calcular
from traductor import traducir
from recordatorios import iniciar_recordatorio, cancelar_recordatorios
from config import HOTKEY, HOTKEY_TEXTO
from perfil import cargar_perfil, guardar_perfil, actualizar_dato

ocupado = False
hablando = False
tray_icon = None
stop_habla = threading.Event()

# Rutas dinámicas según el usuario de Windows actual
_USER = os.environ.get("USERNAME", "")
_APPDATA = os.environ.get("APPDATA", "")
_START_MENU = os.path.join(_APPDATA, "Microsoft", "Windows", "Start Menu", "Programs")

PALABRAS_BUSQUEDA           = ["busca", "busca en internet", "buscar", "googlea", "qué dice internet", "que dice internet", "busca información", "busca informacion"]
PALABRAS_YOUTUBE            = ["busca en youtube", "buscar en youtube", "pon en youtube", "youtube"]
PALABRAS_PANTALLA           = ["pantalla", "mira", "ves", "qué ves", "que ves", "qué hay", "que hay"]
PALABRAS_CAMARA             = ["cámara", "camara", "webcam"]
PALABRAS_ABRIR              = ["abre", "abrir", "lanza", "lanzar", "ejecuta", "ejecutar"]
PALABRAS_CERRAR             = ["cierra", "cerrar", "mata", "cierra la", "cierra el"]
PALABRAS_VOLUMEN_SUBIR      = ["sube el volumen", "subir volumen", "más volumen", "mas volumen", "sube volumen", "volumen más alto", "volumen mas alto"]
PALABRAS_VOLUMEN_BAJAR      = ["baja el volumen", "bajar volumen", "menos volumen", "baja volumen", "volumen más bajo", "volumen mas bajo"]
PALABRAS_SILENCIAR          = ["silencia", "silenciar", "mutealo", "mutea", "sin sonido", "quita el sonido"]
PALABRAS_ACTIVAR_SONIDO     = ["activa el sonido", "desmutealo", "dessilencia", "pon sonido", "quita el mute"]
PALABRAS_VOLUMEN_ACTUAL     = ["qué volumen", "que volumen", "cuánto volumen", "cuanto volumen", "volumen actual"]
PALABRAS_APAGAR             = ["apaga el pc", "apagar el pc", "apaga el ordenador", "apagar ordenador"]
PALABRAS_REINICIAR          = ["reinicia el pc", "reiniciar el pc", "reinicia el ordenador", "reiniciar ordenador"]
PALABRAS_CANCELAR_APAGADO   = ["cancela el apagado", "cancelar apagado", "no apagues"]
PALABRAS_BLOQUEAR           = ["bloquea el pc", "bloquear el pc", "bloquea el ordenador", "bloquea la pantalla"]
PALABRAS_CAPTURA            = ["haz una captura", "captura de pantalla", "screenshot", "haz un screenshot"]
PALABRAS_SIGUIENTE          = ["siguiente canción", "siguiente cancion", "salta la canción", "salta cancion", "pon la siguiente"]
PALABRAS_ANTERIOR           = ["canción anterior", "cancion anterior", "vuelve a la canción", "pon la anterior"]
PALABRAS_PAUSAR             = ["pausa la música", "pausa la musica", "pausa", "para la música", "para la musica"]
PALABRAS_TEMPORIZADOR       = ["ponme un temporizador", "pon un temporizador", "temporizador de", "timer de", "avísame en", "avisame en"]
PALABRAS_CANCELAR_TIMER     = ["cancela el temporizador", "cancelar temporizador", "para el temporizador"]
PALABRAS_ANOTAR             = ["anota", "apunta", "guarda una nota", "escribe que"]
PALABRAS_LEER_NOTAS         = ["lee mis notas", "qué notas tengo", "que notas tengo", "mis notas"]
PALABRAS_PORTAPAPELES       = ["qué tengo copiado", "que tengo copiado", "lee el portapapeles", "qué copié", "que copie"]
PALABRAS_CALCULAR           = ["cuánto es", "cuanto es", "calcula", "cuánto son", "cuanto son"]
PALABRAS_TRADUCIR           = ["traduce", "tradúceme", "traduceme", "cómo se dice", "como se dice"]
PALABRAS_RECORDATORIO       = ["recuérdame", "recuerdame", "ponme un recordatorio", "avísame", "avisame"]
PALABRAS_CANCELAR_RECORDATORIO = ["cancela el recordatorio", "cancelar recordatorio", "cancela los recordatorios"]
PALABRAS_PERFIL_NOMBRE      = ["me llamo", "mi nombre es", "soy "]
PALABRAS_CAMBIAR_VOZ        = ["cambia tu voz", "cambia la voz", "pon voz", "cambia a voz"]

def _app_path(nombre_lnk):
    """Devuelve la ruta al acceso directo en el menú inicio del usuario actual."""
    return os.path.join(_START_MENU, nombre_lnk)

APPS = {
    "spotify":               "spotify",
    "chrome":                "chrome",
    "google chrome":         "chrome",
    "firefox":               "firefox",
    "brave":                 _app_path("Brave.lnk"),
    "discord":               _app_path(os.path.join("Discord Inc", "Discord.lnk")),
    "calculadora":           "calc",
    "notepad":               "notepad",
    "bloc de notas":         "notepad",
    "explorador":            "explorer",
    "archivos":              "explorer",
    "administrador de tareas": "taskmgr",
    "paint":                 "mspaint",
    "steam":                 r"C:\Program Files (x86)\Steam\Steam.exe",
    "navegador":             _app_path("Brave.lnk"),
    "youtube music":         _app_path("YouTube Music.lnk"),
    "música":                _app_path("YouTube Music.lnk"),
    "musica":                _app_path("YouTube Music.lnk"),
    "la música":             _app_path("YouTube Music.lnk"),
    "la musica":             _app_path("YouTube Music.lnk"),
    "whatsapp":              "whatsapp",
    "netflix":               "https://www.netflix.com",
    "twitter":               "https://www.twitter.com",
    "correo":                "https://mail.google.com",
    "instagram":             "https://www.instagram.com",
    "twitch":                "https://www.twitch.tv",
    "x":                     "https://www.twitter.com",
    "claude":                "https://claude.ai/new",
    "tiktok":                "https://tiktok.com",
    "chatgpt":               "https://chat.openai.com",
}

PROCESOS = {
    "spotify":      "Spotify.exe",
    "chrome":       "chrome.exe",
    "firefox":      "firefox.exe",
    "brave":        "brave.exe",
    "discord":      "Discord.exe",
    "steam":        "steam.exe",
    "youtube music":"brave.exe",
    "whatsapp":     "WhatsApp.exe",
    "notepad":      "notepad.exe",
    "paint":        "mspaint.exe",
    "calculadora":  "CalculatorApp.exe",
}

def arrancar_ollama():
    try:
        req.get("http://localhost:11434", timeout=2)
        print("✅ Ollama ya está corriendo.")
    except:
        print("🔄 Arrancando Ollama...")
        subprocess.Popen("ollama serve", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(4)
        print("✅ Ollama arrancado.")

def abrir_app(texto):
    texto_lower = texto.lower()
    for nombre, comando in APPS.items():
        if nombre in texto_lower:
            try:
                if isinstance(comando, str) and comando.startswith("http"):
                    subprocess.Popen(f'start "" "{comando}"', shell=True)
                elif isinstance(comando, str) and (comando.endswith(".lnk") or comando.endswith(".exe")):
                    os.startfile(comando)
                else:
                    subprocess.Popen(comando, shell=True)
                return f"Abriendo {nombre}."
            except Exception as e:
                return f"No pude abrir {nombre}: {e}"
    return None

def cerrar_app(texto):
    texto_lower = texto.lower()
    for nombre, proceso in PROCESOS.items():
        if nombre in texto_lower:
            try:
                subprocess.run(f"taskkill /f /im {proceso}", shell=True, capture_output=True)
                return f"Cerrando {nombre}."
            except Exception as e:
                return f"No pude cerrar {nombre}: {e}"
    return None

def extraer_minutos(texto):
    numeros = re.findall(r'\d+', texto)
    return int(numeros[0]) if numeros else 5

def extraer_query_youtube(texto):
    texto_lower = texto.lower()
    for p in PALABRAS_YOUTUBE:
        texto_lower = texto_lower.replace(p, "").strip()
    return texto_lower

def extraer_nota(texto):
    texto_lower = texto.lower()
    for p in PALABRAS_ANOTAR:
        texto_lower = texto_lower.replace(p, "").strip()
    return texto_lower

def extraer_idioma(texto):
    idiomas = ["inglés", "ingles", "francés", "frances", "alemán", "aleman", "italiano", "portugués", "portugues", "chino", "japonés", "japones"]
    for idioma in idiomas:
        if idioma in texto.lower():
            return idioma
    return "inglés"

def extraer_texto_traducir(texto):
    texto_lower = texto.lower()
    for p in PALABRAS_TRADUCIR:
        texto_lower = texto_lower.replace(p, "").strip()
    for idioma in ["al inglés", "al ingles", "al francés", "al frances", "al alemán", "al aleman", "al italiano", "al chino"]:
        texto_lower = texto_lower.replace(idioma, "").strip()
    return texto_lower

def gestionar_perfil_nombre(texto):
    texto_lower = texto.lower()
    match = re.search(r"(?:me llamo|mi nombre es|soy)\s+([a-záéíóúüñ]+)", texto_lower)
    if match:
        nombre = match.group(1).capitalize()
        actualizar_dato("nombre", nombre)
        return f"Encantada, {nombre}. Ya me acuerdo de tu nombre."
    return None

def gestionar_cambio_voz(texto):
    texto_lower = texto.lower()
    perfil = cargar_perfil()
    opciones = {
        ("masculina", "hombre", "alvaro"):              ("es-ES-AlvaroNeural",    "Voz cambiada a masculina española."),
        ("mexico", "mexicana", "dalia"):                ("es-MX-DaliaNeural",     "Voz cambiada a mexicana."),
        ("argentina", "elena"):                         ("es-AR-ElenaNeural",     "Voz cambiada a argentina."),
        ("femenina", "mujer", "elvira", "española"):    ("es-ES-ElviraNeural",    "Voz cambiada a femenina española."),
        ("inglesa", "inglés", "ingles", "jenny"):       ("en-US-JennyNeural",     "Voice changed to English."),
    }
    for palabras_clave, (nueva_voz, respuesta) in opciones.items():
        if any(p in texto_lower for p in palabras_clave):
            perfil["voz"] = nueva_voz
            guardar_perfil(perfil)
            return respuesta
    return "No reconocí qué voz quieres. Puedes pedir: voz masculina, mexicana, argentina, femenina o inglesa."

def crear_icono_color(color):
    img = Image.new("RGB", (64, 64), color=(30, 30, 30))
    d = ImageDraw.Draw(img)
    d.ellipse([16, 16, 48, 48], fill=color)
    return img

def crear_icono():
    return crear_icono_color((0, 200, 100))

def cambiar_icono(estado):
    global tray_icon
    if tray_icon is None:
        return
    colores = {
        "reposo":     (0, 200, 100),
        "escuchando": (0, 150, 255),
        "pensando":   (255, 200, 0),
        "hablando":   (255, 100, 0),
        "error":      (255, 50, 50),
    }
    color = colores.get(estado, (0, 200, 100))
    try:
        tray_icon.icon = crear_icono_color(color)
        tray_icon.update_menu()
    except:
        pass

def sonido_pensando(stop_event):
    while not stop_event.is_set():
        winsound.Beep(600, 120)
        stop_event.wait(1.2)

def procesar_texto(texto):
    global hablando, stop_habla
    texto_lower = texto.lower()
    stop_pensando = threading.Event()

    try:
        pantalla = capturar_pantalla()

        # — Volumen —
        if any(p in texto_lower for p in PALABRAS_VOLUMEN_SUBIR):
            hablar(subir_volumen(), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_VOLUMEN_BAJAR):
            hablar(bajar_volumen(), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_SILENCIAR):
            hablar(silenciar(), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_ACTIVAR_SONIDO):
            hablar(activar_sonido(), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_VOLUMEN_ACTUAL):
            hablar(volumen_actual(), stop_habla); return

        # — Sistema —
        if any(p in texto_lower for p in PALABRAS_APAGAR):
            hablar(apagar(extraer_minutos(texto_lower)), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_REINICIAR):
            hablar(reiniciar(extraer_minutos(texto_lower)), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_CANCELAR_APAGADO):
            hablar(cancelar_apagado(), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_BLOQUEAR):
            hablar(bloquear(), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_CAPTURA):
            hablar(captura_pantalla(), stop_habla); return

        # — Música —
        if any(p in texto_lower for p in PALABRAS_SIGUIENTE):
            hablar(siguiente_cancion(), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_ANTERIOR):
            hablar(cancion_anterior(), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_PAUSAR):
            hablar(pausar_musica(), stop_habla); return

        # — Temporizadores y recordatorios —
        if any(p in texto_lower for p in PALABRAS_TEMPORIZADOR):
            hablar(iniciar_temporizador(extraer_minutos(texto_lower)), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_CANCELAR_TIMER):
            hablar(cancelar_temporizadores(), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_RECORDATORIO):
            hablar(iniciar_recordatorio(texto, hablar), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_CANCELAR_RECORDATORIO):
            hablar(cancelar_recordatorios(), stop_habla); return

        # — Notas y utilidades —
        if any(p in texto_lower for p in PALABRAS_ANOTAR):
            hablar(anotar(extraer_nota(texto)), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_LEER_NOTAS):
            hablar(leer_notas(), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_PORTAPAPELES):
            hablar(leer_portapapeles(), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_CALCULAR):
            hablar(calcular(texto), stop_habla); return
        if any(p in texto_lower for p in PALABRAS_TRADUCIR):
            hablar(traducir(extraer_texto_traducir(texto), extraer_idioma(texto)), stop_habla); return

        # — Perfil de usuario —
        if any(p in texto_lower for p in PALABRAS_PERFIL_NOMBRE):
            respuesta_nombre = gestionar_perfil_nombre(texto)
            if respuesta_nombre:
                hablar(respuesta_nombre, stop_habla); return

        # — Cambio de voz —
        if any(p in texto_lower for p in PALABRAS_CAMBIAR_VOZ):
            hablar(gestionar_cambio_voz(texto), stop_habla); return

        # — Apps —
        if any(p in texto_lower for p in PALABRAS_ABRIR):
            respuesta_app = abrir_app(texto)
            if respuesta_app:
                cambiar_icono("hablando")
                hablando = True
                hablar(respuesta_app, stop_habla)
                hablando = False
                cambiar_icono("reposo")
                return

        if any(p in texto_lower for p in PALABRAS_YOUTUBE):
            hablar(buscar_youtube(extraer_query_youtube(texto)), stop_habla); return

        if any(p in texto_lower for p in PALABRAS_CERRAR):
            respuesta_cerrar = cerrar_app(texto)
            if respuesta_cerrar:
                cambiar_icono("hablando")
                hablando = True
                hablar(respuesta_cerrar, stop_habla)
                hablando = False
                cambiar_icono("reposo")
                return

        # — IA —
        camara = None
        usar_pantalla = None
        resultados_web = None

        if any(p in texto_lower for p in PALABRAS_CAMARA):
            camara = capturar_camara()
        if any(p in texto_lower for p in PALABRAS_PANTALLA):
            usar_pantalla = pantalla
        if any(p in texto_lower for p in PALABRAS_BUSQUEDA):
            query = texto_lower
            for p in PALABRAS_BUSQUEDA:
                query = query.replace(p, "").strip()
            resultados_web = buscar(query)

        cambiar_icono("pensando")
        hilo_pensando = threading.Thread(target=sonido_pensando, args=(stop_pensando,), daemon=True)
        hilo_pensando.start()

        respuesta = preguntar(texto, usar_pantalla, camara, resultados_web)

        stop_pensando.set()
        hilo_pensando.join(timeout=2)

        if stop_habla.is_set():
            cambiar_icono("reposo")
            return

        winsound.Beep(1100, 100)
        winsound.Beep(880, 100)
        cambiar_icono("hablando")
        hablando = True
        hablar(respuesta, stop_habla)
        hablando = False
        cambiar_icono("reposo")

    except Exception as e:
        stop_pensando.set()
        print(f"Error: {e}")
        cambiar_icono("error")
        winsound.Beep(300, 400)
        threading.Timer(2, lambda: cambiar_icono("reposo")).start()

def on_hotkey():
    global ocupado, hablando, stop_habla

    if hablando:
        stop_habla.set()
        winsound.Beep(400, 150)
        return

    if ocupado:
        winsound.Beep(400, 200)
        return

    ocupado = True
    stop_habla.clear()

    try:
        print("\n⚡ Aria despierta!")

        if esta_en_pantalla_completa():
            winsound.Beep(300, 100)
            return

        cambiar_icono("escuchando")
        winsound.Beep(880, 150)
        winsound.Beep(1100, 150)

        audio = grabar_hasta_silencio()
        texto = transcribir(audio)
        procesar_texto(texto)

    except Exception as e:
        print(f"Error: {e}")
        cambiar_icono("error")
        winsound.Beep(300, 400)
        threading.Timer(2, lambda: cambiar_icono("reposo")).start()
    finally:
        ocupado = False
        hablando = False
        threading.Timer(0.5, lambda: cambiar_icono("reposo")).start()

def on_hotkey_texto():
    global ocupado, hablando, stop_habla

    if ocupado:
        winsound.Beep(400, 200)
        return

    ocupado = True
    stop_habla.clear()

    try:
        cambiar_icono("escuchando")
        winsound.Beep(880, 150)
        texto = pedir_texto()

        if not texto:
            cambiar_icono("reposo")
            return

        print(f"⌨️ Escribiste: {texto}")
        procesar_texto(texto)

    except Exception as e:
        print(f"Error: {e}")
        cambiar_icono("error")
        winsound.Beep(300, 400)
        threading.Timer(2, lambda: cambiar_icono("reposo")).start()
    finally:
        ocupado = False
        hablando = False
        threading.Timer(0.5, lambda: cambiar_icono("reposo")).start()

def escuchar_hotkey():
    print(f"✅ Aria en reposo. Pulsa {HOTKEY.upper()} para voz, {HOTKEY_TEXTO.upper()} para texto.")
    keyboard.add_hotkey(HOTKEY, lambda: threading.Thread(target=on_hotkey).start())
    keyboard.add_hotkey(HOTKEY_TEXTO, lambda: threading.Thread(target=on_hotkey_texto).start())
    keyboard.wait()

def salir(icon, item):
    print("🧠 Guardando memoria de sesión...")
    from ai import historial
    from historial import resumir_sesion
    resumir_sesion(historial)
    icon.stop()
    sys.exit()

def iniciar_tray():
    global tray_icon
    tray_icon = pystray.Icon(
        "Aria",
        crear_icono(),
        "Aria - IA Ambiental",
        menu=pystray.Menu(pystray.MenuItem("Salir", salir))
    )
    tray_icon.run()

if __name__ == "__main__":
    print("🚀 Iniciando Aria...")
    arrancar_ollama()
    t = threading.Thread(target=escuchar_hotkey, daemon=True)
    t.start()
    iniciar_tray()
