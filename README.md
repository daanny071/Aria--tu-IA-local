# 🤖 Aria — IA Ambiental para Windows

<p align="center">
  <img src="assets/ariaimage.png" width="400" alt="Aria Logo">
</p>

Aria es un asistente de inteligencia artificial personal que vive en tu escritorio. Se activa con un hotkey, te escucha, piensa y te responde hablando. **100% gratuito y local** — no necesita ninguna API de pago ni conexión a internet para funcionar.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Windows](https://img.shields.io/badge/Platform-Windows-blue)
![Ollama](https://img.shields.io/badge/IA-Ollama%20local-green)
![Version](https://img.shields.io/badge/Versión-1.1-orange)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green)

---

## ✨ ¿Qué puede hacer Aria?

| Categoría | Ejemplos |
|-----------|----------|
| 💬 Conversación | Responde preguntas, recuerda lo que le cuentas |
| 🧠 Memoria | Recuerda información entre sesiones |
| 👁️ Visión | Ve tu pantalla y cámara cuando se lo pides |
| 🌐 Internet | Busca información actualizada en la web |
| 🖥️ Sistema | Apaga, reinicia, bloquea, capturas de pantalla |
| 🔊 Volumen | Sube, baja, silencia el volumen del PC |
| 🎵 Música | Siguiente canción, anterior, pausa |
| ⏱️ Tiempo | Temporizadores y recordatorios por voz |
| 📝 Notas | Anota y lee notas por voz |
| 🚀 Apps | Abre y cierra aplicaciones con voz |
| 🌍 Idiomas | Detecta el idioma y responde en él |
| 🗣️ Voces | Cambia la voz de Aria al instante |
| 🧮 Cálculos | Resuelve operaciones matemáticas |
| 🌐 Traducir | Traduce frases a varios idiomas |
| 💻 Recursos | RAM, CPU y disco en tiempo real |
| 💰 Crypto | Precio de Bitcoin, Ethereum y más |
| 📅 Calendario | Consulta tus eventos de Google Calendar |
| 📧 Gmail | Lee tus emails sin leer en voz alta |
| 🌤️ Tiempo | Temperatura y previsión al instante |
| 📰 Noticias | Titulares del día por voz |
| 📄 Documentos | Lee PDFs y archivos de texto en voz alta |
| ⌨️ Escritura | Escribe por ti en cualquier campo |
| 🔍 Archivos | Busca archivos por nombre en tu PC |
| 🪟 Ventanas | Mueve y redimensiona ventanas con voz |

---

## 🛠️ Requisitos

- **Windows 10/11**
- **Python 3.10+**
- **[Ollama](https://ollama.com/)** instalado con estos modelos:
  ```
  ollama pull llama3.2
  ollama pull llama3.1:8b
  ollama pull moondream
  ```
- **GPU recomendada** (mínimo 4GB VRAM) o paciencia con CPU
- **Micrófono**

---

## 🚀 Instalación

### 1. Clona el repositorio
```bash
git clone https://github.com/daanny071/aria.git
cd aria
```

### 2. Crea un entorno virtual (recomendado)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4. Instala Ollama y los modelos
Descarga Ollama desde [ollama.com](https://ollama.com/) y luego ejecuta:
```bash
ollama pull llama3.2
ollama pull llama3.1:8b
ollama pull moondream
```

### 5. Configura Aria
Copia `config.example.py` como `config.py` y edítalo:
```bash
copy config.example.py config.py
```
Ajusta:
- **Hotkeys** — por defecto `Alt+Z` (voz) y `Alt+X` (texto)
- **MICRO_INDEX** — si tu micrófono no es el predeterminado, prueba 0, 1, 2...
- **WHISPER_MODEL** — `tiny` (rápido) o `medium` (preciso)
- **TTS_VOICE** — la voz por defecto
- **CIUDAD_TIEMPO** — tu ciudad para el tiempo
- **NEWSDATA_API_KEY** — API key gratuita de [newsdata.io](https://newsdata.io) para noticias

### 6. Google Calendar y Gmail (opcional)
Para conectar con tu cuenta de Google:
1. Crea un proyecto en [Google Cloud Console](https://console.cloud.google.com)
2. Activa las APIs de **Google Calendar** y **Gmail**
3. Crea credenciales OAuth y descarga el `credentials.json`
4. Coloca el archivo en la carpeta de Aria
5. La primera vez que uses el calendario o Gmail, se abrirá el navegador para autorizar

### 7. Arranca Aria
```bash
python main.py
```

Aria aparecerá en la bandeja del sistema con un icono verde 🟢

---

## 🎮 Uso

| Acción | Comando |
|--------|---------|
| Activar por voz | `Alt+Z` |
| Activar por texto | `Alt+X` |
| Interrumpir respuesta | `Alt+Z` mientras habla |
| Cerrar Aria | Clic derecho en el icono → Salir |

### Estados del icono
- 🟢 **Verde** — reposo
- 🔵 **Azul** — escuchando
- 🟡 **Amarillo** — pensando
- 🟠 **Naranja** — hablando
- 🔴 **Rojo** — error

---

## 💬 Comandos de ejemplo

```
"Abre Spotify"
"Sube el volumen"
"Pon un temporizador de 10 minutos"
"Busca en internet el tiempo en Madrid"
"Anota que tengo reunión el lunes"
"¿Qué hay en mi pantalla?"
"Traduce hola al inglés"
"Cambia tu voz a masculina"
"Me llamo Carlos"
"Apaga el PC en 5 minutos"
"¿Cuánta RAM tengo libre?"
"¿Cuánto vale el Bitcoin?"
"¿Qué tengo mañana?"
"¿Tengo emails sin leer?"
"¿Qué tiempo hace?"
"Noticias de hoy"
"Léeme C:\Users\TuNombre\documento.pdf"
"Escribe hola qué tal en el chat"
"Busca el archivo factura"
"Pon Chrome a la izquierda"
"Maximiza Discord"
```

---

## 📁 Estructura del proyecto

```
aria/
├── main.py               # Núcleo principal y hotkeys
├── config.py             # Configuración personal (no se sube)
├── config.example.py     # Plantilla de configuración
├── ai.py                 # Comunicación con Ollama
├── audio.py              # Grabación y transcripción (Whisper)
├── tts.py                # Texto a voz (edge-tts)
├── capture.py            # Captura de pantalla y cámara
├── search.py             # Búsqueda en internet
├── historial.py          # Historial y memoria persistente
├── perfil.py             # Perfil del usuario
├── sistema.py            # Control del sistema Windows
├── volume.py             # Control de volumen
├── notas.py              # Sistema de notas
├── temporizador.py       # Temporizadores
├── recordatorios.py      # Recordatorios
├── calculadora.py        # Cálculos matemáticos
├── traductor.py          # Traducciones
├── utilidades.py         # YouTube, portapapeles
├── nodisturb.py          # Detección pantalla completa
├── input_texto.py        # Input de texto
├── recursos.py           # Monitor RAM, CPU, disco
├── crypto.py             # Precios de criptomonedas
├── buscador_archivos.py  # Búsqueda de archivos
├── google_calendar.py    # Integración Google Calendar
├── gmail.py              # Integración Gmail
├── aviso_diario.py       # Aviso automático a las 20:00
├── tiempo.py             # Previsión meteorológica
├── noticias.py           # Titulares del día
├── lector_docs.py        # Leer PDFs y TXT en voz alta
├── escritura.py          # Escritura por voz en cualquier campo
└── ventanas.py           # Control de ventanas
```

---

## ⚙️ Personalización

### Añadir aplicaciones
En `main.py`, edita el diccionario `APPS`:
```python
APPS = {
    "mi app": r"C:\ruta\a\mi_app.exe",
    ...
}
```

### Cambiar la voz por comando de voz
```
"Cambia tu voz a masculina"
"Cambia tu voz a mexicana"
"Cambia tu voz a argentina"
"Cambia tu voz a inglesa"
```

### Cambiar modelo de IA
Edita `config.py`:
```python
OLLAMA_MODEL = "llama3.2"   # o mistral, gemma2, etc.
```

---

## 🧠 Memoria persistente

Aria guarda un resumen de cada sesión al cerrarse. La próxima vez que arranques, recordará lo que le contaste. Los archivos de memoria son locales y privados:

- `memoria.json` — resúmenes de sesiones anteriores
- `perfil.json` — tu nombre y preferencias
- `historial.txt` — registro completo de conversaciones

Estos archivos están en `.gitignore` y nunca se suben al repositorio.

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Algunas ideas:

- Wake word ("Aria, oye...")
- Integración con WhatsApp
- Leer notificaciones del sistema
- Interfaz gráfica de configuración
- Soporte para más idiomas

---

## 📋 Changelog

### v1.1
- Monitor de recursos — RAM, CPU y disco en tiempo real
- Precios de criptomonedas en tiempo real (CoinGecko)
- Integración con Google Calendar y Gmail
- Previsión meteorológica por voz
- Resumen de noticias del día (NewsData)
- Leer PDFs y archivos de texto en voz alta
- Escritura por voz en cualquier campo del PC
- Búsqueda de archivos por nombre
- Control de ventanas — mover, redimensionar, maximizar
- Saludo con el tiempo al arrancar
- Aviso automático diario a las 20:00 con eventos del día siguiente
- Configuración centralizada en `config.py`

### v1.0
- Lanzamiento inicial

---

## 📄 Licencia

MIT — úsalo, modifícalo y compártelo libremente.

---

*Hecho con Python, Ollama y muchas ganas de tener un J.A.R.V.I.S. propio.*
