import requests
from config import OLLAMA_URL, OLLAMA_MODEL_WEB
from historial import guardar_en_historial, formatear_memoria_para_prompt
from perfil import cargar_perfil

historial = []

def _build_system_prompt():
    perfil = cargar_perfil()
    nombre = perfil.get("datos", {}).get("nombre", "")
    saludo = f"El nombre del usuario es {nombre}. Llámale por su nombre de vez en cuando." if nombre else ""
    memoria = formatear_memoria_para_prompt()

    return f"""Eres Aria, un asistente de IA personal en el ordenador del usuario.
{saludo}
Respondes en el idioma en que te hablen, pero por defecto en español.
Eres amable pero vas al grano, sin rodeos innecesarios.
NUNCA preguntes al usuario si quiere más información, simplemente responde.
NUNCA digas al usuario que visite páginas web, simplemente da la información.
Recuerdas todo lo que el usuario te ha dicho en esta sesión.
{memoria}"""

def _formatear_historial():
    if not historial:
        return "Sin conversación previa."
    resultado = ""
    for h in historial:
        resultado += f"Usuario: {h['usuario']}\nAria: {h['aria']}\n"
    return resultado

def preguntar(texto, imagen_pantalla=None, imagen_camara=None, resultados_web=None):
    global historial

    system_prompt = _build_system_prompt()

    if imagen_pantalla or imagen_camara:
        imgs = []
        if imagen_pantalla:
            imgs.append(imagen_pantalla)
        if imagen_camara:
            imgs.append(imagen_camara)

        payload_vision = {
            "model": "moondream",
            "prompt": f"Describe what you see in this screen in Spanish. The user asks: {texto}",
            "images": imgs,
            "stream": False,
            "options": {"num_predict": 100}
        }
        try:
            print("👁️ Analizando imagen con moondream...")
            r = requests.post(OLLAMA_URL, json=payload_vision, timeout=60)
            descripcion = r.json().get("response", "")
            print(f"👁️ Descripción: {descripcion}")
        except:
            descripcion = ""

        prompt_final = f"{system_prompt}\n\nHistorial de conversación:\n{_formatear_historial()}\n\nEl usuario ha pedido que mires su pantalla. Esto es lo que ves: {descripcion}\n\nUsuario dice: {texto}\n\nResponde directamente."
        modelo = "llama3.2"

    elif resultados_web:
        prompt_final = f"{system_prompt}\n\nHistorial de conversación:\n{_formatear_historial()}\n\nEl usuario preguntó: {texto}\n\nResultados de internet:\n{resultados_web}\n\nUsa SOLO esta información para responder de forma directa. No menciones páginas web."
        modelo = OLLAMA_MODEL_WEB

    else:
        prompt_final = f"{system_prompt}\n\nHistorial de conversación:\n{_formatear_historial()}\n\nUsuario: {texto}\n\nResponde directamente."
        modelo = "llama3.2"

    payload = {
        "model": modelo,
        "prompt": prompt_final,
        "stream": False,
        "options": {
            "num_predict": 150,
            "temperature": 0.3
        }
    }

    try:
        print(f"🤖 Pensando... (modelo: {modelo})")
        respuesta = requests.post(OLLAMA_URL, json=payload, timeout=90)
        data = respuesta.json()
        texto_respuesta = data.get("response", "No pude generar respuesta.")
        print(f"🤖 Aria: {texto_respuesta}")

        historial.append({"usuario": texto, "aria": texto_respuesta})
        guardar_en_historial(texto, texto_respuesta)

        if len(historial) > 10:
            historial = historial[-10:]

        return texto_respuesta
    except Exception as e:
        print(f"Error al contactar Ollama: {e}")
        return "Hubo un error al procesar tu petición."