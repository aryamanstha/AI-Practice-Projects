from pyannote.audio.pipelines.speaker_diarization import SpeakerDiarization
import torch
import os
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.silence import split_on_silence
# from slicer2 import Slicer
import librosa

load_dotenv()

hf_key=os.getenv("HF_ACCESS_TOKEN")

print(hf_key)

pipeline = SpeakerDiarization.from_pretrained("pyannote/speaker-diarization-3.1",use_auth_token=hf_key)

audio_file = "D:\AI-Practice-Projects\\test.wav"

diarization_result = pipeline({"uri": "audio_file", "audio": audio_file})

def detect_silence(audio_file, silence_thresh=-20, min_silence_len=100):
    audio = AudioSegment.from_wav(audio_file)

    non_silent_chunks = split_on_silence(audio,min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    
    silence_intervals = []
    previous_end = 0  
    
    for chunk in non_silent_chunks:
        silence_start = previous_end
        silence_end = silence_start + len(chunk)
        silence_intervals.append((silence_start, silence_end))
        
        previous_end = silence_end

    return silence_intervals

silence_intervals = detect_silence(audio_file)

# for turn, _, speaker in diarization_result.itertracks(yield_label=True):
#     print(f"{turn.start:.2f}s - {turn.end:.2f}s: {speaker}")
    
print("\nDetected Silence Intervals:")
for start_time, end_time in silence_intervals:
    print(f"Silence from {start_time / 1000:.2f}s to {end_time / 1000:.2f}s")
    