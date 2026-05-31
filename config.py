# ─────────────────────────────────────────────
#  Configuración de Aria — edita esto a tu gusto
# ─────────────────────────────────────────────

# Hotkeys para activar Aria
HOTKEY       = "alt+z"   # Voz
HOTKEY_TEXTO = "alt+x"   # Texto escrito

# Ollama
OLLAMA_URL       = "http://localhost:11434/api/generate"
OLLAMA_MODEL     = "llama3.2"        # Modelo principal
OLLAMA_MODEL_WEB = "llama3.1:8b"     # Modelo para búsquedas web

# Voz (edge-tts) — puedes cambiarlo diciendo "cambia la voz a masculina"
TTS_VOICE = "es-ES-AlvaroNeural"

# Audio
SILENCE_SECONDS = 2      # Segundos de silencio para cortar grabación
SAMPLE_RATE     = 16000
WHISPER_MODEL   = "medium"  # tiny | base | small | medium | large
MICRO_INDEX     = 1          # Índice de tu micrófono (0, 1, 2...)

# Rutas
ARIA_DIR             = r"D:\ARIA"
CREDENTIALS_PATH     = r"D:\ARIA\credentials.json"
TOKEN_CALENDAR_PATH  = r"D:\ARIA\token_calendar.pkl"
TOKEN_GMAIL_PATH     = r"D:\ARIA\token_gmail.pkl"

# Google — email de tu cuenta (para añadirte como tester si hace falta)
GOOGLE_EMAIL = "elrobloxiano14@gmail.com"

# Noticias — API key de newsdata.io
NEWSDATA_API_KEY = "TU_API_KEY_AQUI"

# Tiempo — ciudad por defecto
CIUDAD_TIEMPO = "Las Palmas de Gran Canaria"
