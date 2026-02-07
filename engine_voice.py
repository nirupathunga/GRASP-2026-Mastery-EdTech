import os
from deepgram import DeepgramClient # This is the only import you need

# STEP 1: Initialize the Deepgram Client
# It will automatically pick up your DEEPGRAM_API_KEY from the environment
client = DeepgramClient()

def transcribe_file(audio_file_path):
    with open(audio_file_path, "rb") as file:
        buffer_data = file.read()

    # Pass the buffer and options directly
    payload = {"buffer": buffer_data}
    
    # In v5, you pass options like model and smart_format directly as arguments
    options = {
        "model": "nova-3",
        "smart_format": True,
        "language": "en-IN" # Optimized for Indian English
    }

    # Use the rest API endpoint
    response = client.listen.rest.v("1").transcribe_file(payload, options)
    
    # Extract the transcript
    transcript = response.results.channels[0].alternatives[0].transcript
    return transcript