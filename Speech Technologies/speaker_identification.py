from pyannote.audio.pipelines.speaker_diarization import SpeakerDiarization
import torch
import os
from dotenv import load_dotenv
import librosa

load_dotenv()

hf_key=os.getenv("HF_ACCESS_TOKEN")

print(hf_key)

pipeline = SpeakerDiarization.from_pretrained("pyannote/speaker-diarization-3.1",use_auth_token=hf_key)

audio_file = "D:\AI-Practice-Projects\\test.wav"

diarization_result = pipeline({"uri": "audio_file", "audio": audio_file})

speaker_segments = []
for turn, _, speaker in diarization_result.itertracks(yield_label=True):
    speaker_segments.append((turn.start, turn.end, speaker))


speaker_segments.sort(key=lambda x: x[0])

silence_threshold = 0.5 

merged_segments = []
prev_end = 0

for i, (start, end, speaker) in enumerate(speaker_segments):
    
    if start - prev_end > silence_threshold:
        merged_segments.append((prev_end, start, "Silence Detected"))  

    merged_segments.append((start, end, speaker))
    prev_end = end 

print("\nMerged Speaker Diarization and Silence Detection:")
for start, end, label in merged_segments:
    print(f"{start:.2f}s to {end:.2f}s - {label}")