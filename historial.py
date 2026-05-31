import os
import json
import requests
from datetime import datetime

HISTORIAL_PATH = r"D:\ARIA\historial.txt"
MEMORIA_PATH = r"D:\ARIA\memoria.json"
OLLAMA_URL = "http://localhost:11434/api/generate"

# ── Historial de texto plano (igual que antes) ──────────────────────────────

def guardar_en_historial(usuario, aria):
    try:
        with open(HISTORIAL_PATH, "a", encoding="utf-8") as f:
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
            f.write(f"[{fecha}]\n")
            f.write(f"Tú: {usuario}\n")
            f.write(f"Aria: {aria}\n")
            f.write("-" * 40 + "\n")
    except Exception as e:
        print(f"Error guardando historial: {e}")

# ── Memoria persistente ──────────────────────────────────────────────────────

def cargar_memoria():
    """Devuelve la memoria guardada de sesiones anteriores."""
    if not os.path.exists(MEMORIA_PATH):
        return []
    try:
        with open(MEMORIA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def guardar_memoria(memoria):
    try:
        with open(MEMORIA_PATH, "w", encoding="utf-8") as f:
            json.dump(memoria, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando memoria: {e}")

def resumir_sesion(historial_sesion):
    """
    Usa llama3.2 para resumir lo importante de la sesión actual
    y lo añade a la memoria persistente.
    """
    if not historial_sesion:
        return

    # Construir texto de la sesión
    texto_sesion = ""
    for h in historial_sesion:
        texto_sesion += f"Usuario: {h['usuario']}\nAria: {h['aria']}\n"

    prompt = f"""Analiza esta conversación entre un usuario y Aria (su asistente de IA) y extrae SOLO la información personal o relevante que Aria debería recordar en futuras sesiones.

Extrae cosas como:
- Datos personales mencionados (trabajo, familia, gustos, rutinas)
- Proyectos o tareas en curso
- Preferencias expresadas
- Problemas que tenía y si se resolvieron
- Cualquier cosa que el usuario quiera que se recuerde

Si no hay nada relevante que recordar, responde exactamente: NADA

Conversación:
{texto_sesion}

Responde en español con viñetas cortas, sin preamble, solo la lista o NADA."""

    try:
        respuesta = requests.post(OLLAMA_URL, json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": 200, "temperature": 0.2}
        }, timeout=60)
        resumen = respuesta.json().get("response", "").strip()

        if resumen and resumen.upper() != "NADA":
            memoria = cargar_memoria()
            fecha = datetime.now().strftime("%d/%m/%Y")
            memoria.append({
                "fecha": fecha,
                "resumen": resumen
            })
            # Máximo 30 entradas, si no empieza a ser demasiado contexto
            if len(memoria) > 30:
                memoria = memoria[-30:]
            guardar_memoria(memoria)
            print(f"🧠 Memoria actualizada con {len(resumen)} caracteres.")
    except Exception as e:
        print(f"Error generando resumen de sesión: {e}")

def formatear_memoria_para_prompt():
    """Devuelve la memoria en formato texto para incluir en el prompt de Aria."""
    memoria = cargar_memoria()
    if not memoria:
        return ""

    texto = "Información que recuerdas de sesiones anteriores con este usuario:\n"
    for entrada in memoria[-10:]:  # Solo las últimas 10 entradas
        texto += f"[{entrada['fecha']}] {entrada['resumen']}\n"
    return texto