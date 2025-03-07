import torch
import torchaudio
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice

# Initialize the TTS model
tts = TextToSpeech()

# Text to convert to speech
text = "Hello, how are you today? I hope you are doing well."

# Load a voice (e.g., "random" for a generic voice)
voice = "random"

# Generate speech
gen = tts.tts(text, voice=voice)

# Save the output
torchaudio.save("output.wav", gen.squeeze(0).cpu(), 24000)

print("Audio saved as output.wav")