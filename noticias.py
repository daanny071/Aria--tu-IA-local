import requests
from config import NEWSDATA_API_KEY

def obtener_noticias(tema=None):
    try:
        query = tema if tema else "noticias España hoy"
        url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&language=es&q={query}&size=5"
        r = requests.get(url, timeout=10)
        data = r.json()

        articulos = data.get("results", [])
        if not articulos:
            return "No encontré noticias ahora mismo."

        respuesta = f"Aquí van las noticias {'sobre ' + tema if tema else 'de hoy'}. "
        for i, art in enumerate(articulos[:5], 1):
            titulo = art.get("title", "Sin título")
            respuesta += f"{i}. {titulo}. "

        return respuesta
    except Exception as e:
        return f"No pude obtener las noticias: {e}"
