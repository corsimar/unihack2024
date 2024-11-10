import streamlit as st
import openai
import sounddevice as sd
import numpy as np
import io
from pydub import AudioSegment

# Set your OpenAI API key

def record_audio(duration=5, fs=44100):
    """Record audio for a specified duration in seconds."""
    st.write("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    audio = audio.flatten()
    st.write("Recording finished.")
    return audio, fs

def audio_to_wav(audio, fs):
    """Convert numpy array audio to WAV format."""
    audio_segment = AudioSegment(
        data=audio.tobytes(),
        sample_width=audio.dtype.itemsize,
        frame_rate=fs,
        channels=1
    )
    wav_io = io.BytesIO()
    audio_segment.export(wav_io, format="wav")
    return wav_io

def transcribe_audio(audio_data):
    """Send audio to OpenAI Whisper for transcription."""
    # Seek to the start of the BytesIO object before sending to OpenAI API
    audio_data.seek(0)
    
    response = openai.Audio.transcriptions.create(
        model="whisper-1", 
        file=audio_data,
        response_format="text"  # Optional: specify text-only response
    )
    transcription = response["text"]
    return transcription

# Streamlit App
st.title("Live Transcription with Whisper")

st.write("Click the button to start recording and transcribing.")

if st.button("Start Recording"):
    # Record 5 seconds of audio
    duration = 5  # seconds
    audio, fs = record_audio(duration=duration)
    audio_data = audio_to_wav(audio, fs)
    
    # Transcribe audio
    transcription = transcribe_audio(audio_data)
    
    st.write("Transcription:")
    st.write(transcription)
