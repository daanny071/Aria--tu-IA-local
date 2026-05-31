import os
from datetime import datetime

NOTAS_PATH = r"D:\ARIA\notas.txt"

def anotar(texto):
    try:
        with open(NOTAS_PATH, "a", encoding="utf-8") as f:
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
            f.write(f"[{fecha}] {texto}\n")
        return f"Anotado."
    except Exception as e:
        return f"No pude anotar: {e}"

def leer_notas():
    try:
        if not os.path.exists(NOTAS_PATH):
            return "No tienes notas guardadas."
        with open(NOTAS_PATH, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
        if not contenido:
            return "No tienes notas guardadas."
        lineas = contenido.split("\n")
        ultimas = lineas[-5:]
        return "Tus últimas notas son: " + ". ".join(ultimas)
    except Exception as e:
        return f"No pude leer las notas: {e}"