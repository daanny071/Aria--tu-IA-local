from langdetect import detect

VOCES = {
    "es": "es-ES-ElviraNeural",
    "en": "en-US-JennyNeural",
    "fr": "fr-FR-DeniseNeural",
    "de": "de-DE-KatjaNeural",
    "it": "it-IT-ElsaNeural",
    "pt": "pt-BR-FranciscaNeural",
}

def detectar_idioma(texto):
    try:
        return detect(texto)
    except:
        return "es"

def voz_para_idioma(idioma):
    return VOCES.get(idioma, VOCES["es"])