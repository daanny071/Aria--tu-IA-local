import requests
from config import CIUDAD_TIEMPO

def obtener_tiempo(ciudad=None):
    if not ciudad:
        ciudad = CIUDAD_TIEMPO
    try:
        url = f"https://wttr.in/{ciudad.replace(' ', '+')}?format=j1"
        r = requests.get(url, timeout=10)
        data = r.json()

        actual = data["current_condition"][0]
        temp = actual["temp_C"]
        sensacion = actual["FeelsLikeC"]
        descripcion = actual["lang_es"][0]["value"] if actual.get("lang_es") else actual["weatherDesc"][0]["value"]
        humedad = actual["humidity"]
        viento = actual["windspeedKmph"]

        manana = data["weather"][1]
        max_temp = manana["maxtempC"]
        min_temp = manana["mintempC"]
        desc_manana = manana["hourly"][4]["lang_es"][0]["value"] if manana["hourly"][4].get("lang_es") else ""

        return (
            f"En {ciudad} ahora mismo hay {temp} grados, sensación de {sensacion}. "
            f"{descripcion}. Humedad al {humedad}% y viento a {viento} kilómetros por hora. "
            f"Mañana entre {min_temp} y {max_temp} grados, {desc_manana}."
        )
    except Exception as e:
        return "No pude obtener el tiempo ahora mismo."
