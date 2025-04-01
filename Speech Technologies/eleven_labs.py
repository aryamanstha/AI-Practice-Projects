from dotenv import load_dotenv
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import streamlit as st
import io

st.title("Eleven Labs Text-to-Speech Demo")

load_dotenv()

client=ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

voices={
    "Charlotte":"XB0fDUnXU5powFXDhCwa",
    "Aria":"9BWtsMINqrJLrRacOk9x",
    "Bill":"pqHfZKP75CvOlQylNhV4",
    "Elli":"MF3mGyEYCl7XYWbV9V6O",
}
def generate_audio(voice_id,text):
    audio = client.text_to_speech.convert(
    text=text,
    voice_id=voice_id,
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(audio)  
    return audio_bytes

selected_voice = st.selectbox("Choose a voice:", list(voices.keys()))
text_input = st.text_area("Enter text to convert to speech:", "This is the demo for the Eleven Labs API.")


if st.button("Generate Audio"):
    voice_id = voices[selected_voice]
    audio = generate_audio(voice_id, text_input)
    audio_stream = io.BytesIO(audio)
    
    st.audio(audio_stream, format="audio/mp3")
    
    st.download_button("Download Audio", audio_stream, file_name="speech.mp3", mime="audio/mp3")
    
# if __name__ == "__main__":
#     print("Choose a voice:")
#     for idx,name in enumerate(voices):
#         print(f"{idx+1}: {name}")
#     choice = int(input("Enter the number of the voice you want to use: "))
#     voice_id = list(voices.values())[choice-1]
#     audio = generate_audio(voice_id)
#     play(audio)
#     print("Audio played successfully.")
