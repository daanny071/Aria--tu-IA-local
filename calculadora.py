import re
import math

def calcular(texto):
    try:
        texto = texto.lower()
        texto = texto.replace("más", "+").replace("menos", "-")
        texto = texto.replace("por", "*").replace("entre", "/")
        texto = texto.replace("al cuadrado", "**2").replace("raíz de", "math.sqrt(")
        
        # Porcentajes: "15% de 340"
        porcentaje = re.search(r'(\d+(?:\.\d+)?)\s*%\s*de\s*(\d+(?:\.\d+)?)', texto)
        if porcentaje:
            p = float(porcentaje.group(1))
            n = float(porcentaje.group(2))
            resultado = (p / 100) * n
            return f"{p}% de {n} es {resultado}."

        # Extrae solo números y operadores
        expresion = re.sub(r'[^0-9+\-*/().\s]', '', texto).strip()
        if expresion:
            resultado = eval(expresion)
            return f"El resultado es {resultado}."
        return "No entendí la operación."
    except:
        return "No pude calcular eso."