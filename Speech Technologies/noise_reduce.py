import noisereduce as nr
from pydub import AudioSegment
from pydub.effects import normalize
import librosa
import numpy as np
import soundfile as sf

def remove_noise(audio_path, temp_output_path):
    
    y, sr = librosa.load(audio_path, sr=None)
    reduced_noise = nr.reduce_noise(y=y, sr=sr, prop_decrease=0.8)
    
    sf.write(temp_output_path, reduced_noise, sr)
    
def normalize_audio(input_path, output_path):
    audio = AudioSegment.from_wav(input_path)
    normalized_audio = audio.normalize()

    normalized_audio.export(output_path, format="wav")
    print(f"Normalized audio saved as {output_path}")

# Example usage
temp_wav = "temp_denoised.wav"
final_output = "output.wav"


if __name__ == "__main__":
    temp_wav = "temp_denoised.wav"
    final_output = "final_output.wav"
    
    input_audio = "D:\AI-Practice-Projects\sample_audio.wav"  
    remove_noise(input_audio, temp_wav)
    normalize_audio(temp_wav, final_output)
