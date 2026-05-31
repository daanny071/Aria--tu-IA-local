import subprocess
import urllib.parse
import tkinter as tk

def buscar_youtube(query):
    query_limpia = query.strip()
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query_limpia)}"
    subprocess.Popen(f'start "" "{url}"', shell=True)
    return f"Buscando {query_limpia} en YouTube."

def leer_portapapeles():
    try:
        root = tk.Tk()
        root.withdraw()
        contenido = root.clipboard_get()
        root.destroy()
        if not contenido:
            return "El portapapeles está vacío."
        if len(contenido) > 200:
            return f"Tienes copiado un texto largo. Empieza así: {contenido[:200]}"
        return f"Tienes copiado: {contenido}"
    except:
        return "No hay nada copiado."