from ddgs import DDGS

def traducir(texto, idioma_destino="inglés"):
    idiomas = {
        "inglés": "English",
        "ingles": "English", 
        "francés": "French",
        "frances": "French",
        "alemán": "German",
        "aleman": "German",
        "italiano": "Italian",
        "portugués": "Portuguese",
        "portugues": "Portuguese",
        "chino": "Chinese",
        "japonés": "Japanese",
        "japones": "Japanese",
    }

    idioma = idiomas.get(idioma_destino.lower(), "English")

    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.translate([texto], to=idioma))
            if resultados:
                return f"En {idioma_destino}: {resultados[0]['translated']}"
    except:
        pass

    return f"No pude traducir el texto."