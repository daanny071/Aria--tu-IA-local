import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os
from faster_whisper import WhisperModel
from config import SAMPLE_RATE, SILENCE_SECONDS, WHISPER_MODEL, MICRO_INDEX

modelo_whisper = None

def cargar_whisper():
    global modelo_whisper
    if modelo_whisper is None:
        print("Cargando Whisper...")
        modelo_whisper = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
        print("Whisper listo.")

def grabar_hasta_silencio():
    print("🎙️ Escuchando...")
    chunk = int(SAMPLE_RATE * 0.5)
    grabado = []
    silencio_count = 0
    max_silencio = int(SILENCE_SECONDS / 0.5)

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", device=MICRO_INDEX) as stream:
        while True:
            audio_chunk, _ = stream.read(chunk)
            grabado.append(audio_chunk.copy())
            volumen = np.abs(audio_chunk).mean()
            if volumen < 0.005:
                silencio_count += 1
            else:
                silencio_count = 0
            if silencio_count >= max_silencio and len(grabado) > max_silencio:
                break

    audio = np.concatenate(grabado, axis=0)
    return audio

def transcribir(audio):
    cargar_whisper()
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_name = tmp.name
    tmp.close()
    wav.write(tmp_name, SAMPLE_RATE, (audio * 32767).astype(np.int16))
    segmentos, _ = modelo_whisper.transcribe(tmp_name, language="es")
    texto = " ".join([s.text for s in segmentos]).strip()
    try:
        os.unlink(tmp_name)
    except:
        pass
    print(f"🗣️ Dijiste: {texto}")
    return texto