from ddgs import DDGS

def buscar(query, max_results=3):
    try:
        print(f"🔍 Buscando: {query}")
        with DDGS() as ddgs:
            resultados = list(ddgs.text(query, max_results=max_results))
        if not resultados:
            return "No encontré resultados para esa búsqueda."
        resumen = ""
        for r in resultados:
            resumen += f"- {r['title']}: {r['body']}\n"
        return resumen
    except Exception as e:
        print(f"Error buscando: {e}")
        return "No pude conectarme a internet para buscar."