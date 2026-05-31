import json
import os

PERFIL_PATH = os.path.join(os.path.dirname(__file__), "perfil.json")

PERFIL_DEFAULT = {
    "nombre": "",
    "idioma_preferido": "es",
    "voz": "es-ES-ElviraNeural",
    "preferencias": [],
    "datos": {}
}

def cargar_perfil():
    if os.path.exists(PERFIL_PATH):
        with open(PERFIL_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return PERFIL_DEFAULT.copy()

def guardar_perfil(perfil):
    with open(PERFIL_PATH, "w", encoding="utf-8") as f:
        json.dump(perfil, f, ensure_ascii=False, indent=2)

def actualizar_dato(clave, valor):
    perfil = cargar_perfil()
    perfil["datos"][clave] = valor
    guardar_perfil(perfil)

def obtener_dato(clave, default=None):
    perfil = cargar_perfil()
    return perfil["datos"].get(clave, default)