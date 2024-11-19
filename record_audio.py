import sounddevice as sd
import wavio
import numpy as np
from datetime import datetime
import os 

today = datetime.today().strftime('%Y-%m-%d')

def record_audio(filename, sample_rate=44100):
    print("Recording... Press Enter to stop.")
    
    # Create target directory if it doesn't exist
    directory = f"./user_inputs/{today}/"
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist

    # Record audio
    audio_data = []
    def callback(indata, frames, time, status):
        audio_data.append(indata.copy())
    
    with sd.InputStream(samplerate=sample_rate, channels=1, callback=callback):
        input()  # Wait for user to press Enter
        print("Recording stopped.")

    # Combine recorded audio data and save as .wav
    audio_data = np.concatenate(audio_data, axis=0)
    file_path = os.path.join(directory, filename + ".wav")  # Save as .wav
    wavio.write(file_path, audio_data, sample_rate, sampwidth=2)
    print(f"Audio saved at {file_path}")
    return file_path
