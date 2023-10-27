import os
import sys
import json
import random
import time
from vosk import Model, KaldiRecognizer
import pyaudio

MODEL_PATH = r"C:\vosk"
if not os.path.exists(MODEL_PATH):
    print("Proszę rozpakować model do odpowiedniego katalogu lub zmienić ścieżkę.")
    sys.exit(1)

model = Model(MODEL_PATH)

# Ustawienia mikrofonu i Voska
sample_rate = 16000
rec = KaldiRecognizer(model, sample_rate)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=8000)
stream.start_stream()

# Mapowanie słowne dla liczb
number_map = {
    "jeden": 1,
    "dwa": 2,
    "trzy": 3,
    "cztery": 4,
    "pięć": 5,
    "sześć": 6,
    "siedem": 7,
    "osiem": 8,
    "dziewięć": 9,
    "dziesięć": 10
}

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')  # Wyczyść konsolę (dla Windows 'cls', dla innych systemów 'clear')

while True:
    clear_console()  # Wyczyść konsolę przed wyświetleniem nowej liczby
    target_number = random.randint(1, 10)
    print(f"Proszę powiedzieć liczbę: {target_number}")

    recognized_text = ""
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            recognized_text = result.get("text", "").lower()
            
            print(f"Rozpoznano: {recognized_text}")

            recognized_number = number_map.get(recognized_text, None)
            if recognized_number == target_number:
                print("!!! Brawo !!!")
                time.sleep(4)  # Poczekaj 5 sekund przed wyświetleniem nowej liczby
                break
            else:
                print("Spróbuj jeszcze raz")

stream.stop_stream()
stream.close()
p.terminate()
